from azure_conection import AzureConnection
from openai_connection import OpenAIConnection

def main():
    text = OpenAIConnection.conversation()
    AzureConnection.text_to_speech(text)
    
if __name__ == "__main__":
    main()