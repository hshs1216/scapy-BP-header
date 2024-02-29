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
#define DEST_PORT 12345      // 送信先のポート番号

void *send_function(void *arg) {
    int sockfd = *((int *)arg);
    struct sockaddr_in destaddr;
    char message[] = "Hello from sender";

    // 送信先のアドレス情報の設定
    memset(&destaddr, 0, sizeof(destaddr));
    destaddr.sin_family = AF_INET;
    destaddr.sin_port = htons(DEST_PORT);
    inet_pton(AF_INET, arg, &destaddr.sin_addr);

    // メッセージの送信
    while (1) {
        if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *)&destaddr, sizeof(destaddr)) < 0) {
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

    // ソケットの作成
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    // サーバーのアドレス情報の設定
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(12345);

    // ソケットにアドレスをバインド
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // 送信スレッドの作成
    if (pthread_create(&send_thread, NULL, send_function, argv[1]) != 0) {
        perror("pthread_create failed");
        exit(EXIT_FAILURE);
    }

    // データの受信
    while (1) {
        addrlen = sizeof(cliaddr);
        recvlen = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr *)&cliaddr, &addrlen);
        if (recvlen < 0) {
            perror("recvfrom failed");
            exit(EXIT_FAILURE);
        }

        // 受信したデータの表示
        buffer[recvlen] = '\0';
        printf("Received: %s\n", buffer);
    }

    // ソケットのクローズ
    close(sockfd);

    return 0;
}
