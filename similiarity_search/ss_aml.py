from sentence_transformers import SentenceTransformer
import numpy as np

# 加载模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    return model.encode(text, convert_to_tensor=True)

def embed_texts(texts):
    return model.encode(texts, convert_to_tensor=True)



if __name__ == "__main__":
# 使用示例
    query = "2023年硅谷银行破产的原因是什么？"
    text_chunks = [
    "Regulators pointed out serious problems in Silicon Valley Bank's risk management...",
    "In March 2023, Silicon Valley Bank experienced a bank run due to a liquidity crisis...",
    "Task 3: Check system logs for abnormal records.",
    "Task 4: Update server security patches and restart the system.",
    "Task 5: Back up the database and verify data integrity.",
    "Task 6: Monitor network traffic to detect potential attacks.",
    "Task 7: Organize and categorize user feedback.",
    "Task 8: Write automated test scripts for regression testing.",
    "Task 9: Optimize code performance to reduce response time.",
    "Task 10: Analyze recent system crash logs.",
    "Task 11: Design a new user interface prototype.",
    "Task 12: Test the compatibility of new functional modules.",
    "Task 13: Review the security reports of third-party services.",
    "Task 14: Update project documentation and release the latest version.",
    "Task 15: Connect to external API interfaces for data synchronization.",
    "Task 16: Evaluate the security of data encryption schemes.",
    "Task 17: Check cloud service configurations and optimize resource allocation.",
    "Task 18: Write error handling and logging mechanisms.",
    "Task 19: Monitor application performance metrics and generate reports.",
    "Task 20: Debug issues in the user permission management module.",
    "Task 21: Configure firewall rules to prevent unauthorized access.",
    "Task 22: Implement data cleaning processes to improve data quality.",
    "Task 23: Integrate various system modules for comprehensive testing.",
    "Federal Reserve rate hike, interest rates increased.",
    "Task 25: Deploy the new version to the test environment for evaluation.",
    "Task 26: Analyze user behavior data to improve product experience.",
    "Task 27: Implement continuous integration and continuous deployment solutions.",
    "Task 28: Monitor log servers and set up alert notifications.",
    "Task 29: Review the codebase to eliminate potential security vulnerabilities.",
    "Task 30: Optimize database queries to improve response speed."
]
