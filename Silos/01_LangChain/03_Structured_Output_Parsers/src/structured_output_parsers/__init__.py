from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))

class Item(BaseModel):
    name: str = Field(description="Name of item")
    category: str = Field(description="Category of item")

def main():
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", max_output_tokens=40, temperature=0)
    parser = JsonOutputParser(pydantic_object=Item)
    prompt = PromptTemplate(
        template="Classify item: {item}.\n{format_instructions}",
        input_variables=["item"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    res = chain.invoke({"item": "Apple"})
    print(f"Parsed Object: {res}")

if __name__ == "__main__":
    main()
