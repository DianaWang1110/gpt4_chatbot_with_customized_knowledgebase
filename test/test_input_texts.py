from website_vectordb_query.main_functions import *

# test with valid inputs
query1 = f"""
    Dear Mr. Robertson,

    I hope this message finds you well. Could you please provide more details about the Egnyte's enterprise solution? 
    In particular, I'm interested in storage capabilities, integration options, and the pricing plans for this package.

    Best regards,
    Olivia
"""
system_msg1 = f"""You are an AI assistant. Please, help Mr.Robertson in addressing Olivia's inquiries about Egnyte's enterprise solution, including storage capabilities, integration options, and pricing."""

# test with invalid inputs
query2 = "12345678"
system_msg2 = f""" You are a helpful AI assistant. Respond to this email on behalf of our sales representative
    and answer any questions the email entails.
"""

# test with edge cases
query3 = "Hello Mr. Smith, " + "a" * 10000 + "Can you please tell me about Egnyte's pricing plans?"
system_msg3 = f"""You are an AI assistant. Respond to the query, keeping in mind the length and complexity of the question."""


query4 = f"""
    Hello Mr. Smith,

    I was wondering what Egnyte's pricing plans are for the following special use cases:
    1. Collaboration with clients in countries that use non-Latin characters (e.g., Japanese, Arabic, Russian).
    2. Secure storage and sharing of files that contain sensitive data (#$%@!&*).

    Sincerely,
    Joe
"""
system_msg4 = f"""You are Mr.Smith, a sales representative at Egnyte. Address Joe's concerns about Egnyte's capabilities for non-Latin characters and sensitive data handling."""

sage_url = "https://www.sage.com/en-us/"
egnyte_url = "https://www.egnyte.com/"

queries = [query1, query2, query3, query4]
system_msgs = [system_msg1, system_msg2, system_msg3, system_msg4]

def create_query_vectordb(query, system_msg):
    augmented_query = create_augmented_query_vectordb("egnyte", query)
    test_augmented_query(augmented_query, system_msg)
def main():
    for query, system_msg in zip(queries, system_msgs):
        create_query_vectordb(query, system_msg)

if __name__ == '__main__':
    main()





