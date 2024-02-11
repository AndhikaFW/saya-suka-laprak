from typing import Annotated
import shutil

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import os
import glob
import time
from dotenv import load_dotenv                                 
load_dotenv()                                                  
api_key = os.getenv("OPENAI_API_KEY")
checkpause = os.getenv("PAUSE")
from llama_index.llms import OpenAI                            
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.schema import Document
from pathlib import Path
import time

docs_chat = FastAPI()

docs_chat.mount("/static", StaticFiles(directory="static"), name="static")

def llamaindex(query_engine, task):
                                                                                         
    response = query_engine.query(task)                                                   

    return response;


@docs_chat.post("/prompt/")
async def create_upload_files(title: Annotated[str, Form(...)], text0: Annotated[str, Form(...)], text1: Annotated[str, Form(...)], text2: Annotated[str, Form(...)], text3: Annotated[str, Form(...)], text4: Annotated[str, Form(...)], files: list[UploadFile] = File(...),):
        for file in files:
            try:
                file_location = f"data/{file.filename}"
                path = Path(file_location)
                if not path.is_file():
                    with open(file_location, "wb+") as file_object:
                        shutil.copyfileobj(file.file, file_object)
            except Exception:
                return {"filenames": f"{[file.filename for file in files]} failed to upload"}
            finally:              
                await file.close()
        #return {"title": title,
            #   "text0": text0,
            #   "text1": text1,
            #   "text2": text2,
            #   "text3": text3,
            #   "text4": text4}
        if checkpause == "True":
            pause = 60;
        else:
            pause = 0;

        inputDocs = [f"data/{file.filename}" for file in files];
        documents = SimpleDirectoryReader(input_files=inputDocs).load_data()

        #Custom                                                                                   
        from llama_index import ServiceContext, set_global_service_context                        
                                                                                          
        #define LLM:                                                                              
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)                        
        #configure service context                                                                
        service_context = ServiceContext.from_defaults(llm=llm, chunk_size=1000, chunk_overlap=20)
        #set_global_service_context(service_context)                                              
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)       
 
        docs = index.as_query_engine()   

        task = f"Buatkan prinsip dasar untuk praktikum { title }"

        p0 = llamaindex(docs, task)
        time.sleep(pause)

        task = f"Berikut merupakan teori tambahan singkat untuk praktikum { title }: ({ text0 }), Buatkan teori tambahan untuk praktikum { title }"

        p1 = llamaindex(docs, task)
        time.sleep(pause)

        task = f"Berikut merupakan analisis percobaan singkat untuk praktikum { title }: ({ text1 }), Buatkan analisis percobaan untuk praktikum { title }"
                                                                                                                                             
        p2 = llamaindex(docs, task)
        time.sleep(pause)

        task = f"Berikut merupakan analisis hasil singkat untuk praktikum { title }: ({ text2 }), Buatkan analisis hasil untuk praktikum { title }"
                                                                                                                                             
        p3 = llamaindex(docs, task)
        time.sleep(pause)
 
        task = f"Berikut merupakan analisis kesalahan singkat untuk praktikum { title }: ({ text3 }), Buatkan analisis kesalahan untuk praktikum { title }"
                                                                                                                                             
        p4 = llamaindex(docs, task)
        time.sleep(pause)

        task = f"Berikut merupakan kesimpulan singkat untuk praktikum { title }: ({ text4 }), berdasarkan analisis: ({ p2 }{ p3 }),  Buatkan kesimpulan untuk praktikum { title }"
                                                                                                                                             
        p5 = llamaindex(docs, task)

        pagecontent = f"""<!DOCTYPE html>                                                                                                                                                                                             
        <html lang="en">                                                                                                                                                                                            
            <head>                                                                                                                                                                                                    
                <title>📚 Generator isi Laprak</title>                                                                                                                                                                   
                <meta charset="UTF-8">                                                                                                                                                                                  
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>                                                                                                                                                                                                   
            <body style="font-family: Helvetica, sans-serif;color: #fafafa;background-color: #0e1117;">                                                                                                                                                                                                    
                <ul style="width: 90%; margin: 0 auto; text-align: center; background-color: #262730; border-radius: 8px;">                                                                                                                                                                                                                                             
                    <li style="position: absolute; left: 0px; margin: 17px auto auto 5%; display: inline-block; width:10%;">                                                                                                                                                                                                                                            
                        <button style="cursor: pointer; color: #fafafa; height:100%; background-color: transparent; border: none;overflow: hidden;outline: none;" onclick="history.back()">                                                                                                                                                                             
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">                                                                                                                                                                                                                                                       
                                <path fill="currentColor" d="M16.62 2.99a1.25 1.25 0 0 0-1.77 0L6.54 11.3a.996.996 0 0 0 0 1.41l8.31 8.31c.49.49 1.28.49 1.77 0s.49-1.28 0-1.77L9.38 12l7.25-7.25c.48-.48.48-1.28-.01-1.76"/>                                                                                                                                           
                            </svg>                                                                                                                                                                                                                                                                                                                                      
                        </button>                                                                                                                                                                                                                                                                                                                                       
                    </li><li style="display: inline-block; width:80%;">                                                                                                                                                                                                                                                                                                 
                        <p style="padding-right: 10%">Refresh page untuk ulang pertanyaan - Kembali untuk pertanyaan baru</p>                                                                                                                                                                                                                                           
                    </li><li style="position: absolute; right:0; margin: 17px 5% auto auto; display:inline-block; width:10%;">                                                                                                                                                                                                                                          
                        <button style="cursor: pointer; color: #fafafa; height:100%; background-color: transparent; border: none;overflow: hidden;outline: none;" onclick="printPage()">                                                                                                                                                                                
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">                                                                                                                                                                                                                                                       
                                <path fill="currentColor" d="M19 8H5c-1.66 0-3 1.34-3 3v4c0 1.1.9 2 2 2h2v2c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2v-2h2c1.1 0 2-.9 2-2v-4c0-1.66-1.34-3-3-3m-4 11H9c-.55 0-1-.45-1-1v-4h8v4c0 .55-.45 1-1 1m4-7c-.55 0-1-.45-1-1s.45-1 1-1s1 .45 1 1s-.45 1-1 1m-2-9H7c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h10c.55 0 1-.45 1-1V4c0-.55-.45-1-1-1"/>
                            </svg>                                                                                                                                                                                                                                                                                                                                      
                        </button>                                                                                                                                                                                                                                                                                                                                       
                    </li>                                                                                                                                                                                                                                                                                                                                               
                </ul>                                                                                                                                                                                                                                                                                                                                                   
                <div id="GFG" style="padding:20px 5% 0; white-space: pre-wrap">
                    <h2><b>{ title }</b></h2><br>
                    <h3><b>Prinsip Dasar</b></h3><br>
                    { p0 }<br><br>
                    <h3><b>Teori Tambahan</b></h3><br>
                    { p1 }<br>
                    <h3><b>Analisis Percobaan</b></h3><br>
                    { p2 }<br>                        
                    <h3><b>Analisis Hasil</b></h3><br>
                    { p3 }<br>                        
                    <h3><b>Analisis Kesalahan</b></h3><br>
                    { p4 }<br>                        
                    <h3><b>Kesimpulan</b></h3><br>
                    { p5 }             
                </div>
            </body>
            <script src="../static/js/print.js"></script>
        </html>"""                                                                                                                                                                                                     
        return HTMLResponse(content=pagecontent)
@docs_chat.get("/")
async def main():
    return FileResponse('index.html')

