// Web3 Service for Ethereum wallet interactions

class Web3Service {
  constructor() {
    this.web3 = null;
    this.account = null;
    this.isConnected = false;
  }

  // Check if MetaMask is installed
  isMetaMaskInstalled() {
    return typeof window.ethereum !== 'undefined';
  }

  // Connect to MetaMask wallet
  async connectWallet() {
    if (!this.isMetaMaskInstalled()) {
      throw new Error('MetaMask is not installed. Please install MetaMask to continue.');
    }

    try {
      // Request account access
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });

      if (accounts.length === 0) {
        throw new Error('No accounts found. Please make sure your wallet is unlocked.');
      }

      this.account = accounts[0];
      this.isConnected = true;

      // Listen for account changes
      this.setupEventListeners();

      return this.account;
    } catch (error) {
      if (error.code === 4001) {
        throw new Error('User rejected the connection request.');
      }
      throw new Error(`Failed to connect wallet: ${error.message}`);
    }
  }

  // Get current connected account
  async getCurrentAccount() {
    if (!this.isMetaMaskInstalled()) {
      return null;
    }

    try {
      const accounts = await window.ethereum.request({
        method: 'eth_accounts'
      });
      
      if (accounts.length > 0) {
        this.account = accounts[0];
        this.isConnected = true;
        return this.account;
      }
      
      return null;
    } catch (error) {
      console.error('Error getting current account:', error);
      return null;
    }
  }

  // Disconnect wallet (clear local state)
  async disconnectWallet() {
    this.account = null;
    this.isConnected = false;
    this.removeEventListeners();
    return true;
  }

  // Get wallet balance
  async getBalance(address = null) {
    if (!this.isMetaMaskInstalled()) {
      throw new Error('MetaMask is not installed');
    }

    const targetAddress = address || this.account;
    if (!targetAddress) {
      throw new Error('No wallet address available');
    }

    try {
      const balance = await window.ethereum.request({
        method: 'eth_getBalance',
        params: [targetAddress, 'latest']
      });

      // Convert from wei to ether
      const balanceInEther = parseInt(balance, 16) / Math.pow(10, 18);
      return balanceInEther.toFixed(4);
    } catch (error) {
      throw new Error(`Failed to get balance: ${error.message}`);
    }
  }

  // Get network information
  async getNetwork() {
    if (!this.isMetaMaskInstalled()) {
      throw new Error('MetaMask is not installed');
    }

    try {
      const chainId = await window.ethereum.request({
        method: 'eth_chainId'
      });

      const networks = {
        '0x1': 'Ethereum Mainnet',
        '0x3': 'Ropsten Testnet',
        '0x4': 'Rinkeby Testnet',
        '0x5': 'Goerli Testnet',
        '0x2a': 'Kovan Testnet',
        '0x61': 'BSC Testnet',
        '0x38': 'BSC Mainnet',
        '0x89': 'Polygon Mainnet',
        '0x13881': 'Polygon Mumbai'
      };

      return {
        chainId,
        name: networks[chainId] || 'Unknown Network'
      };
    } catch (error) {
      throw new Error(`Failed to get network: ${error.message}`);
    }
  }

  // Switch to a specific network
  async switchNetwork(chainId) {
    if (!this.isMetaMaskInstalled()) {
      throw new Error('MetaMask is not installed');
    }

    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId }]
      });
    } catch (error) {
      if (error.code === 4902) {
        throw new Error('Network not added to MetaMask');
      }
      throw new Error(`Failed to switch network: ${error.message}`);
    }
  }

  // Setup event listeners for account and network changes
  setupEventListeners() {
    if (!this.isMetaMaskInstalled()) return;

    // Account changed
    window.ethereum.on('accountsChanged', (accounts) => {
      if (accounts.length === 0) {
        this.disconnectWallet();
      } else {
        this.account = accounts[0];
      }
    });

    // Network changed
    window.ethereum.on('chainChanged', (chainId) => {
      // Reload the page when network changes
      window.location.reload();
    });

    // Connection changed
    window.ethereum.on('connect', (connectInfo) => {
      console.log('Wallet connected:', connectInfo);
    });

    window.ethereum.on('disconnect', (error) => {
      console.log('Wallet disconnected:', error);
      this.disconnectWallet();
    });
  }

  // Remove event listeners
  removeEventListeners() {
    if (!this.isMetaMaskInstalled()) return;

    window.ethereum.removeAllListeners('accountsChanged');
    window.ethereum.removeAllListeners('chainChanged');
    window.ethereum.removeAllListeners('connect');
    window.ethereum.removeAllListeners('disconnect');
  }

  // Format address for display
  formatAddress(address, length = 4) {
    if (!address) return '';
    return `${address.substring(0, length + 2)}...${address.substring(address.length - length)}`;
  }

  // Validate Ethereum address
  isValidAddress(address) {
    return /^0x[a-fA-F0-9]{40}$/.test(address);
  }
}

// Create singleton instance
const web3Service = new Web3Service();

export default web3Service;