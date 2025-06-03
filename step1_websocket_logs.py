"""
Step 1: WebSocket logs subscriber for Solana real-time transaction monitoring
"""
import asyncio
import websockets
import json
from datetime import datetime

class SolanaLogsSubscriber:
    """
    Step 1: WebSocket client để nhận real-time logs từ Solana
    """
    def __init__(self, network="devnet"):
        if network == "testnet":
            self.websocket_url = "wss://api.testnet.solana.com"
            self.http_rpc_url = "https://api.testnet.solana.com"
        elif network == "mainnet":
            self.websocket_url = "wss://api.mainnet-beta.solana.com"
            self.http_rpc_url = "https://api.mainnet-beta.solana.com"
        elif network == "devnet":
            self.websocket_url = "wss://api.devnet.solana.com"
            self.http_rpc_url = "https://api.devnet.solana.com"
        else:
            raise ValueError("Network must be 'testnet', 'mainnet', or 'devnet'")
        
        self.network = network # Lựa chọn mạng lưới: testnet hoặc mainnet
        self.websocket = None # Biến để lưu kết nối WebSocket
        self.subscription_id = None # ID của subscription (nếu có)
        
        print(f"STEP 1: ĐĂNG KÝ WEBSOCKET LOGS")
        print(f"Network: {network}")
        print(f"WebSocket URL: {self.websocket_url}")
    
    async def connect(self):
        """
        Bước 1a: Kết nối WebSocket
        """
        print("\nBƯỚC 1A: KẾT NỐI WEBSOCKET")
        print("-" * 30)
        print(f"URL: {self.websocket_url}")
        
        try:
            self.websocket = await websockets.connect(
                self.websocket_url, 
                ping_timeout=30,
                close_timeout=10
            )
            print("Kết nối WebSocket thành công!")
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
    
    async def subscribe_wallet_logs(self, wallet_address):
        """
        Bước 1B: Đăng ký nhận logs của ví cụ thể
        """
        print(f"\nBƯỚC 1B: ĐĂNG KÝ WALLET LOGS")
        print("-" * 40)
        print(f"Wallet: {wallet_address}")
        
        subscription_request = {
            "jsonrpc": "2.0", 
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {
                    "mentions": [wallet_address]
                },
                {
                    "commitment": "finalized"
                }
            ]
        }
        
        print("Wallet subscription request:")
        print(json.dumps(subscription_request, indent=2))
        
        await self.websocket.send(json.dumps(subscription_request))
        
        response = await self.websocket.recv()
        response_data = json.loads(response)
        
        if "result" in response_data:
            self.subscription_id = response_data["result"]
            print(f"Wallet subscription thành công! ID: {self.subscription_id}")
            return True
        else:
            print(f"Wallet subscription thất bại: {response_data}")
            return False
    
    async def listen_for_notifications(self, max_notifications=5):
        """
        Bước 1C: Lắng nghe notifications
        """
        print(f"\nBƯỚC 1C: LẮNG NGHE NOTIFICATIONS")
        print("-" * 40)
        print(f"Số lượng notifications tối đa: {max_notifications}") # Giới hạn số lượng notifications để nhận
        print("Đang chờ logs...")
        
        notification_count = 0 # Biến đếm số lượng notifications đã nhận
        
        # Lặp để nhận logs
        while notification_count < max_notifications:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=60)
                data = json.loads(message)
                
                if "method" in data and data["method"] == "logsNotification":
                    notification_count += 1
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    print(f"\n[{timestamp}] NOTIFICATION #{notification_count}")
                    print("-" * 25)
                    
                    result = data["params"]["result"]
                    signature = result["value"]["signature"]
                    logs = result["value"]["logs"]
                    error = result["value"]["err"]
                    
                    print(f"Signature: {signature}")
                    print(f"Status: {'SUCCESS' if error is None else 'FAILED'}")
                    print(f"Log count: {len(logs)}")
                    print("First 3 logs:")
                    
                    for i, log_line in enumerate(logs[:3]):
                        print(f"  {i+1}. {log_line}")
                    
                    if len(logs) > 3:
                        print(f"  ... and {len(logs) - 3} more logs")
                    
                else:
                    print(f"Other message: {data.get('method', 'unknown')}")
                    
            except asyncio.TimeoutError:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Timeout - No transactions in 60s")
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        print(f"\nStep 1 hoàn thành! Đã nhận {notification_count} notifications")
        return notification_count
    
    async def close(self):
        """
        Đóng kết nối
        """
        if self.websocket:
            await self.websocket.close()
            print("Đã đóng WebSocket connection")
