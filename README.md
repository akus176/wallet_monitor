# Hệ Thống Giám Sát Giao Dịch Solana

Hệ thống giám sát giao dịch real-time cho blockchain Solana, được phát triển bằng Python.

## Cấu Trúc Dự Án

```
├── data_structures.py          # Mô hình dữ liệu (TransactionDetails)
├── step1_websocket_logs.py     # WebSocket logs subscriber 
├── step2_transaction_details.py # HTTP transaction details fetcher
├── wallet_monitor.py           # Lớp monitor tổng hợp
├── main.py                     # Điểm khởi chạy chính và các hàm demo
├── requirements.txt            # Các thư viện Python cần thiết
├── README.md                   # File này
└── Transaction_Monitor.py      # File gốc (để tham khảo)
```

## Các Thành Phần

### 1. `data_structures.py`
- Chứa dataclass `TransactionDetails`
- Định dạng có cấu trúc cho dữ liệu giao dịch đã được parse

### 2. `step1_websocket_logs.py`
- Lớp `SolanaLogsSubscriber`
- WebSocket client để nhận logs Solana real-time
- Xử lý subscription cho logs của ví cụ thể hoặc tất cả logs

### 3. `step2_transaction_details.py`
- Lớp `SolanaTransactionDetailsFetcher`  
- HTTP client để lấy thông tin chi tiết giao dịch
- Parse dữ liệu giao dịch thô thành định dạng có cấu trúc

### 4. `wallet_monitor.py`
- Lớp `SolanaWalletMonitor`
- Kết hợp WebSocket logs + HTTP details fetching
- Chức năng giám sát chính

### 5. `main.py`
- Điểm khởi chạy ứng dụng
- Các hàm demo và giao diện người dùng
- Lựa chọn network và cấu hình

## Cài Đặt

```bash
pip install -r requirements.txt
```

## Cách Sử Dụng

### Chạy monitor chính:
```bash
python main.py
```

### Import các thành phần riêng lẻ:
```python
from wallet_monitor import SolanaWalletMonitor
from data_structures import TransactionDetails
```

## Tính Năng

- Giám sát giao dịch real-time thông qua WebSocket của Solana
- Parse chi tiết giao dịch thông qua HTTP RPC (API của Solana)
- Hỗ trợ Devnet, Testnet và Mainnet
- Logic retry tự động và rate limiting
- Phát hiện loại giao dịch (chuyển SOL, chuyển token, v.v.)
- Theo dõi thay đổi số dư
- Thống kê hiệu suất

## Hỗ Trợ Network

- **Devnet**: Mạng phát triển để thử nghiệm
- **Testnet**: Mạng thử nghiệm với test tokens  
- **Mainnet**: Mạng Solana production

## Ví Dụ Đầu Ra

```
TÓM TẮT GIAO DỊCH #1
────────────────────────────────────────
Signature: 2Kzg9x5C3mP8nQ7fR1bV8...
Thời gian: 2025-06-03 10:30:45 UTC
Slot: 123,456,789
Phí: 0.000005000 SOL
Loại: SOL_TRANSFER
Trạng thái: SUCCESS

CHI TIẾT CHUYỂN KHOẢN:
Từ: 8mK2vN4pQ7xR9tY5wZ1eF6gH...
Đến: 3nL8qW2rT6yU4sA9pM5dK7hJ...
Số lượng: 0.100000000 SOL
```