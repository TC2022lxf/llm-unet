from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		"Hello!!",	# str  in 'parameter_3' Textbox component
		api_name="/update"
)
print(result)