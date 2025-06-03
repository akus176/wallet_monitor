import asyncio
from wallet_monitor import SolanaWalletMonitor

async def main():
    print("SOLANA WALLET TRANSACTION MONITOR")
    print("="*50)
    print("Real-time monitoring với full transaction details")
    print("="*50)
    
    # Network selection
    print("\nChọn Solana network:")
    print("1. Devnet")
    print("2. Testnet")
    print("3. Mainnet")
    
    network_choice = input("\nChọn network (1/2/3, mặc định 1-Devnet): ").strip()
    
    if network_choice == "2":
        network = "testnet"
        print("Đã chọn Testnet")
    elif network_choice == "3":
        network = "mainnet"
        print("Đã chọn Mainnet")
    else:
        network = "devnet"
        print("Đã chọn Devnet")
    
    monitor = SolanaWalletMonitor(network)
    
    try:
        if not await monitor.connect():
            print("Không thể kết nối WebSocket")
            return
        
        wallet = input("\nNhập địa chỉ ví cần monitor: ").strip()
        
        if not wallet:
            print("Cần nhập địa chỉ ví!")
            return
        
        max_tx = input("Số transactions tối đa (mặc định 5): ").strip()
        max_tx = int(max_tx) if max_tx.isdigit() else 5
        
        await monitor.monitor_wallet(wallet, max_tx)
        
    except KeyboardInterrupt:
        print("\nDừng monitoring bởi người dùng")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        await monitor.close()

if __name__ == "__main__":
    asyncio.run(main())