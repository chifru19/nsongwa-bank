# Use a secure, slim version of Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install curl for the healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security (BankUser)
RUN useradd -m bankuser

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bank app code
COPY . .

# Grant the non-root user ownership of the app files
RUN chown -R bankuser:bankuser /app

# Ensure the database directory is persistent
VOLUME /app/instance

# Switch to the non-root user
USER bankuser

# Expose the port the app runs on
EXPOSE 5000

# Healthcheck to ensure the banking portal is responsive
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/login || exit 1

# Start the bank application
CMD ["python", "app.py"]