# Networks Final Project: CDN Scraper

## Project Overview

This project is part of CS514: Advanced Computer Networks at Duke University. The goal is to design and evaluate a system that allows a client to obtain all locations of CDN servers and choose the best responding CDN servers independently, without relying on DNS resolution.

## Problem Statement

DNS-based CDNs use the geolocation of a client’s DNS resolver’s IP address to find the best CDN server for a client. This process is error-prone as both IP geo-location and the client’s resolver’s IP address can be incorrect. The objective is to create a system that mitigates these issues by enabling clients to directly query and evaluate CDN servers.

## Solution Design

### System Architecture

1. **CDN Server Discovery**: The system will query a list of known CDN providers to obtain the IP addresses of their servers.
2. **Latency Measurement**: The client will measure the latency to each CDN server using ICMP ping or HTTP requests.
3. **Server Selection**: The client will select the CDN server with the lowest latency.

### Components

- **CDN Scraper**: A module to query CDN providers and retrieve server IP addresses.
- **Latency Tester**: A module to measure the latency to each CDN server.
- **Server Selector**: A module to choose the best CDN server based on latency measurements.

## Evaluation

The system will be evaluated based on:

- **Accuracy**: How well the selected CDN server performs compared to the DNS-based selection.
- **Efficiency**: The time taken to discover and evaluate CDN servers.
- **Reliability**: The consistency of the selected CDN server's performance over multiple tests.

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Networks-CDNServerChoice.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Networks-CDNServerChoice
    ```
3. Run XXX:
    ```sh
    python XXX.py
    ```

## Conclusion

This project aims to provide a more accurate and reliable method for clients to select the best CDN server by bypassing the traditional DNS-based approach. By directly measuring latency, clients can make more informed decisions, leading to improved performance and user experience.

## References

Minyuan Zhou, Xiao Zhang, Shuai Hao, Xiaowei Yang, Jiaqi Zheng, Guihai Chen, and Wanchun Dou. Regional ip anycast: Deployments, performance, and potentials. In Proceedings of the ACM SIGCOMM 2023 Conference, 2023.

## Contributors

- Stella Gong
- Lilly Grella
- Brendan Massey


## License

This project is licensed under the MIT License.