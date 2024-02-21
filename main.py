from website import create_app
from openai import OpenAI

app = create_app()

if(__name__ == '__main__'): # We now have a running web server, but only if this file is run directly
    app.run(debug=True) # run flask application, debug=true means it will automatically rerun when we make a change (turn this off in production)






# SAVED FOR FUTURE USE

# client = OpenAI(api_key="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")

# input_data = str(input("Enter notes: "))


# stream = client.chat.completions.create(
#     model="gpt-3.5-turbo-0125",
#     messages=[{"role": "user", "content": f"Make flashcards with this content: {input_data}"}],
#     stream=True,
# )


# data_array = []
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         data_array.append(chunk.choices[0].delta.content, end="") 