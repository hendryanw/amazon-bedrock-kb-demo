# Amazon Bedrock Knowledge Bases Demo

## Prerequisites
1. Setup [Bedrock knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
2. Setup [AWS CLI](https://aws.amazon.com/cli/) profile with sufficient permissions

## Running the Application

1. Set your Bedrock knowledge base ID in the `bedrock_kb` variable within `/app/app.py` file.
2. Install requirements `pip install -r requirements.txt`
3. Run the Streamlit application using
    ```
    streamlit run app/app.py
    ```