"""this library Automates the creation of a Langchain Chat object"""

import os
import glob
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import NotebookLoader, pdf, JSONLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter, MarkdownTextSplitter

from langchain_core.output_parsers import StrOutputParser


from langchain_core.runnables import RunnablePassthrough


from openad.helpers.output import output_error, output_warning


from openad.llm_assist.model_reference import get_tell_me_model


from openad.llm_assist.model_reference import get_embeddings_model


def len_func(text):
    return len(text)


class Chatobject:
    """This is the Chat Object that is instantiated once per session"""

    llm_service = None
    llm_model = None
    organisation = None
    target = None
    API_key = None
    vector_db = None
    db_handle = None
    chat_history = []
    db_dir = "~/.vector_embed"
    document_folders = ["./"]
    document_types = ["**/*.txt", "**/*.ipynb", "**/*.run", "**/*.cdoc", "**/*.pdf", "**/*.md"]

    def __init__(
        self,
        target="OPENAPI",
        organisation=None,
        API_key=None,
        vector_db="FAISS",
        document_folders=["./"],
        document_types=document_types,
        db_dir_override=None,
        refresh_vector=False,
        llm_model="instructlab/granite-7b-lab",
        llm_service="ollama",
    ):
        self.organisation = organisation
        self.target = target
        self.API_key = API_key
        self.vector_db = vector_db
        self.db_handle = None
        self.document_folders = document_folders
        self.document_types = document_types
        self.llm_service = llm_service
        self.llm_model = llm_model

        if db_dir_override is not None and os.path.exists(os.path.expanduser(db_dir_override)) is True:
            self.db_dir = db_dir_override
        if self.vector_db == "FAISS":
            try:
                self.db_handle = self.load_faiss_db(refresh_vector)
                if self.db_handle is False:
                    raise RuntimeError(f"Failed to load embeddings for service {self.llm_service}")
            except (ConnectionError, TimeoutError) as e:
                raise ConnectionError(f"Failed to connect to embeddings service: {e}") from e
            except (FileNotFoundError, PermissionError) as e:
                raise RuntimeError(f"Failed to access vector database: {e}") from e
            except Exception as e:
                raise RuntimeError(f"Failed to load vector database: {e}") from e
        else:
            raise ValueError(f"Vector database '{self.vector_db}' is not currently supported")

    def prime_chat_history(self, primer: str):
        """ "add the prompt tuning text primer to the chat"""
        self.chat_history.append((primer, "ok"))

    def load_faiss_db(self, refresh=True):
        """Load the Faiss Database Embeddings"""
        ###########################################################################
        # validation Testing

        main_db = None

        embeddings = get_embeddings_model(self.llm_service, self.API_key)

        if embeddings is False:
            return False

        if refresh is not True:
            try:
                if self.vector_db == "FAISS":
                    main_db = FAISS.load_local(
                        os.path.expanduser(self.db_dir + "/faiss_index"),
                        embeddings,
                        allow_dangerous_deserialization=True,
                    )  # pylint: disable=no-member
                return main_db
            except FileNotFoundError:
                # Database not found, force a refresh
                output_warning("FAISS index not found, creating new embeddings", return_val=False)
                refresh = True
            except (PermissionError, OSError) as e:
                output_error(f"Failed to access FAISS index: {e}", return_val=False)
                return False
            except Exception as e:
                output_warning(f"Failed to load existing FAISS index, creating new: {e}", return_val=False)
                refresh = True

        docs = []
        # Instruct the user as the tool has detected a change in underlying toolkt or workspace that it will update the FAISS index
        output_warning("Updating Embeddings for current Toolkits and Workspaces", return_val=False)
        try:
            # excluded_files=[]
            for i in self.document_folders:
                for j in self.document_types:
                    if j == "**/*.ipynb":
                        for file in glob.glob(i + "/*.ipynb"):
                            loader = NotebookLoader(
                                file,
                                include_outputs=False,
                                max_output_length=20,
                                remove_newline=False,
                            )
                            try:
                                documents = loader.load()
                                text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=3000, chunk_overlap=0, separators=[","]
                                )
                                # docs.extend(text_splitter.split_documents(documents))
                            except (ValueError, RuntimeError):
                                # Some notebook files are not processable, skip them silently
                                # to avoid overwhelming users with many error messages
                                pass
                            except Exception as e:
                                output_warning(f"Failed to process notebook {file}: {e}", return_val=False)
                    elif j == "**/*.pdf":
                        loader = DirectoryLoader(i, glob=j, loader_cls=pdf.BasePDFLoader)
                        documents = loader.load()
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000, chunk_overlap=30, separators=["\\@"], keep_separator=False
                        )
                        docs.extend(text_splitter.split_documents(documents))
                    elif j == "**/*.md":
                        loader = DirectoryLoader(i, glob=j, loader_cls=UnstructuredMarkdownLoader)
                        try:
                            documents = loader.load()
                            headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
                            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

                            text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size=2000,
                                chunk_overlap=30,
                                separators=["\\@"],
                                length_function=len_func,
                                keep_separator=False,
                            )
                            for doc in documents:
                                docs.extend(
                                    text_splitter.split_documents(markdown_splitter.split_text(doc.page_content))
                                )
                        except (ValueError, RuntimeError) as e:
                            output_warning(f"Failed to process markdown file: {e}", return_val=False)
                        except Exception as e:
                            output_warning(f"Unexpected error processing markdown: {e}", return_val=False)
                    elif j == "**/*.json":
                        loader = DirectoryLoader(
                            i,
                            glob=j,
                            loader_cls=JSONLoader,
                            loader_kwargs={"jq_schema": ".", "text_content": False},
                        )
                        try:
                            documents = loader.lazy_load()
                            docs.extend(documents)
                        except (ValueError, RuntimeError) as e:
                            output_warning(f"Failed to process JSON file: {e}", return_val=False)
                        except Exception as e:
                            output_warning(f"Unexpected error processing JSON: {e}", return_val=False)
                    elif j == "**/*.cdoc":
                        loader = DirectoryLoader(i, glob=j, loader_cls=TextLoader)
                        documents = loader.load()
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=2000, chunk_overlap=30, separators=["\\@", "Property:"], keep_separator=False
                        )
                        docs.extend(text_splitter.split_documents(documents))
                    else:
                        loader = DirectoryLoader(i, glob=j, loader_cls=TextLoader)
                        documents = loader.load()
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=2000, chunk_overlap=30, separators=["\n"]
                        )
                        docs.extend(text_splitter.split_documents(documents))

            main_db = FAISS.from_documents(docs, embeddings)  # pylint: disable=no-member

            main_db.save_local(os.path.expanduser(self.db_dir + "/faiss_index"))

        except (ConnectionError, TimeoutError) as e:
            output_error(f"Failed to connect to embeddings service: {e}", return_val=False)
            return False
        except (OSError, PermissionError) as e:
            output_error(f"Failed to save vector database: {e}", return_val=False)
            return False
        except Exception as e:
            output_error(f"Unexpected error creating vector database: {e}", return_val=False)
            return False
        return main_db

    def how_to_search(self, search: str):
        """Executing the Tell Me Function"""
        retriever = self.db_handle.as_retriever(k=100)

        model, template = get_tell_me_model(self.llm_service, self.API_key)

        if model is None:
            return "No Answer Could Be Generated, Error Connecting to Model"
        try:
            from langchain_core.runnables import RunnableLambda

            def inspect(state):
                """Print the state passed between Runnables in a langchain and pass it on"""
                # print(state)
                return state

            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | RunnableLambda(inspect)
                | prompt
                | model
                | StrOutputParser()
            )

            question = search
            answers = None

            try:
                result = chain.invoke(question)
            except (ConnectionError, TimeoutError) as e:
                return output_error(f"Failed to connect to LLM service: {e}", return_val=True)
            except Exception as e:
                return output_error(f"Unable to execute LLM request: {e}", return_val=True)
        except (ConnectionError, TimeoutError) as e:
            return output_error(f"Failed to connect to LLM service: {e}", return_val=True)
        except Exception as e:
            return output_error(f"Failed querying LLM: {e}", return_val=True)
        try:
            # self.chat_history.append((question, result["answer"]))
            if len(self.chat_history) > 3:
                try:
                    self.chat_history.remove(2)
                except (IndexError, ValueError):
                    # Chat history manipulation failed, not critical
                    pass
            if self.llm_service == "BAM":
                result = result.split("Answer:")[-1].strip()

            answers = "<green>Question:</green> <yellow>" + question + "</yellow>\n\n" + result

        except Exception as e:  # pylint: disable=broad-exception-caught
            return output_error("Unable to Execute Request: " + str(e), return_val=True)
        return answers
