#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUF_SIZE 1024

int main() {
    int sockfd;
    struct sockaddr_in servaddr, cliaddr;
    char buffer[BUF_SIZE];
    socklen_t addrlen;
    ssize_t recvlen;

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

    // データの受信
    addrlen = sizeof(cliaddr);
    recvlen = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr *)&cliaddr, &addrlen);
    if (recvlen < 0) {
        perror("recvfrom failed");
        exit(EXIT_FAILURE);
    }

    // 受信したデータの表示
    buffer[recvlen] = '\0';
    printf("Received: %s\n", buffer);

    // ソケットのクローズ
    close(sockfd);

    return 0;
}
