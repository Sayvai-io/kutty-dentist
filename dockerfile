From continuumio/miniconda3:latest

WORKDIR /app

EXPOSE 5000

#Copy environment.yml
COPY environment.yml .

#Run
RUN conda env create -f environment.yml
RUN conda activate ast
RUN echo "checking....for..dependencies"
RUN python3 -c "import fastapi"

#Copy everything 
COPY . .
# Run uvicorn when the container launches
CMD ["uvicorn", "main:app", "--port", "8000", "--reload"]