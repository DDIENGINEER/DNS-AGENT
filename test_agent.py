from app.agent import ask_dns_agent

question = """
Check api.com and api.example.com across private and public DNS.
Validate resolution in all regions and identify hosting.
"""

result = ask_dns_agent(question)

print("\n===== DNS AI ASSISTANT =====\n")
print(result)