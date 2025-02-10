FROM pgvector/pgvector:pg17

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-all

# Clone, build, and install pgvector
RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/