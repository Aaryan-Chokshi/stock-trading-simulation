# Use the official Go image as a base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Go source code into the container
COPY hello.go .

# Compile the Go program
RUN go build hello.go

# Run the compiled program
CMD ["./hello"]

