FROM public.ecr.aws/lambda/python:3.11

# Copy entire backend directory
# Lambda needs access to all modules:
# shared/, repositories/, services/,
# routers/, models/
COPY . ${LAMBDA_TASK_ROOT}

# Install all dependencies
RUN pip install --no-cache-dir \
  psycopg2-binary==2.9.9 \
  boto3==1.34.0 \
  xgboost==2.0.3 \
  pandas==2.1.4 \
  numpy==1.26.3 \
  scikit-learn==1.3.2 \
  scipy==1.11.4

# Handler: file path . function name
CMD ["lambdas/ingestion/handler.handler"]
