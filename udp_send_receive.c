#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define BUF_SIZE 1024
#define DEST_PORT 12345

typedef struct {
    int sockfd;
    char dest_ip[INET_ADDRSTRLEN];
} thread_args_t;

void *send_function(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    struct sockaddr_in destaddr;
    char message[] = "Hello from sender";

    memset(&destaddr, 0, sizeof(destaddr));
    destaddr.sin_family = AF_INET;
    destaddr.sin_port = htons(DEST_PORT);
    inet_pton(AF_INET, args->dest_ip, &destaddr.sin_addr);

    while (1) {
        if (sendto(args->sockfd, message, strlen(message), 0, (struct sockaddr *)&destaddr, sizeof(destaddr)) < 0) {
            perror("sendto failed");
            exit(EXIT_FAILURE);
        }
        printf("Sent: %s\n", message);
        sleep(5);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <destination IP address>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int sockfd;
    struct sockaddr_in servaddr, cliaddr;
    char buffer[BUF_SIZE];
    socklen_t addrlen;
    ssize_t recvlen;
    pthread_t send_thread;
    thread_args_t args;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(12345);

    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    args.sockfd = sockfd;
    strncpy(args.dest_ip, argv[1], INET_ADDRSTRLEN);

    if (pthread_create(&send_thread, NULL, send_function, &args) != 0) {
        perror("pthread_create failed");
        exit(EXIT_FAILURE);
    }

    while (1) {
        addrlen = sizeof(cliaddr);
        recvlen = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr *)&cliaddr, &addrlen);
        if (recvlen < 0) {
            perror("recvfrom failed");
            exit(EXIT_FAILURE);
        }

        buffer[recvlen] = '\0';
        printf("Received: %s\n", buffer);
    }

    close(sockfd);

    return 0;
}
``
