#! /usr/bin/bash
pip freeze | grep -E "(langchain)|(dotenv)|(langgraph)" > requirements.txt