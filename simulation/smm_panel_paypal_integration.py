"""
SMM Panel PayPal Integration Implementation
Practical integration example for GoUpSocial and YtAboneHilesi providers
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import hmac
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderStatus(Enum):
    CREATED = "created"
    PROCESSING = "processing"
    PARTIAL = "partial"
    COMPLETED = "completed"
    CANCELED = "canceled"

class SMMProviderConfig:
    """Configuration for SMM panel providers"""
    
    GOUPSOCIAL = {
        "name": "GoUpSocial",
        "api_url": "https://goupsocial.com/api/v2",
        "api_key": "YOUR_GOUPSOCIAL_API_KEY",
        "supports_refill": True,
        "supports_cancel": True,
        "min_order_amount": 0.10,
        "max_order_amount": 10000.00
    }
    
    YTABONEHILESI = {
        "name": "YtAboneHilesi",
        "api_url": "https://ytabonehilesi.com/api",  # Hypothetical API
        "api_key": "YOUR_YTABONEHILESI_API_KEY",
        "supports_refill": False,
        "supports_cancel": False,
        "min_order_amount": 0.05,
        "max_order_amount": 1000.00,
        "focus_platform": "youtube"
    }

class PayPalIntegration:
    """PayPal payment processing integration"""
    
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        self.base_url = "https://api.sandbox.paypal.com" if sandbox else "https://api.paypal.com"
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> str:
        """Get PayPal access token"""
        if self.access_token and self.token_expires_at > datetime.now():
            return self.access_token
        
        auth_url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        
        data = "grant_type=client_credentials"
        
        response = requests.post(
            auth_url,
            headers=headers,
            data=data,
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data["expires_in"]
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.access_token
        else:
            raise Exception(f"Failed to get PayPal access token: {response.text}")
    
    def create_payment(self, amount: float, currency: str = "USD", 
                      description: str = "", return_url: str = "", 
                      cancel_url: str = "") -> Dict:
        """Create PayPal payment"""
        token = self.get_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        payment_data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                },
                "description": description
            }],
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "payment_method": {
                    "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                }
            }
        }
        
        response = requests.post(
            f"{self.base_url}/v2/checkout/orders",
            headers=headers,
            json=payment_data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create PayPal payment: {response.text}")
    
    def capture_payment(self, order_id: str) -> Dict:
        """Capture PayPal payment"""
        token = self.get_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(
            f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
            headers=headers
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to capture PayPal payment: {response.text}")

class SMMProviderClient:
    """Generic SMM provider client"""
    
    def __init__(self, provider_config: Dict):
        self.config = provider_config
        self.api_url = provider_config["api_url"]
        self.api_key = provider_config["api_key"]
        self.name = provider_config["name"]
    
    def get_services(self) -> List[Dict]:
        """Get available services from provider"""
        payload = {
            "key": self.api_key,
            "action": "services"
        }
        
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get services from {self.name}: {response.text}")
    
    def place_order(self, service_id: int, link: str, quantity: int) -> Dict:
        """Place order with SMM provider"""
        payload = {
            "key": self.api_key,
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity
        }
        
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to place order with {self.name}: {response.text}")
    
    def get_order_status(self, order_id: int) -> Dict:
        """Get order status from provider"""
        payload = {
            "key": self.api_key,
            "action": "status",
            "order": order_id
        }
        
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get order status from {self.name}: {response.text}")
    
    def get_balance(self) -> Dict:
        """Get account balance from provider"""
        payload = {
            "key": self.api_key,
            "action": "balance"
        }
        
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get balance from {self.name}: {response.text}")

class SMMPanelManager:
    """Main SMM panel management class with PayPal integration"""
    
    def __init__(self, paypal_client_id: str, paypal_client_secret: str, 
                 sandbox: bool = True):
        self.paypal = PayPalIntegration(paypal_client_id, paypal_client_secret, sandbox)
        self.providers = {
            "goupsocial": SMMProviderClient(SMMProviderConfig.GOUPSOCIAL),
            "ytabonehilesi": SMMProviderClient(SMMProviderConfig.YTABONEHILESI)
        }
        self.orders = {}  # In production, use database
        self.payments = {}  # In production, use database
    
    def calculate_pricing(self, provider_name: str, service_id: int, 
                         quantity: int) -> Dict:
        """Calculate pricing including PayPal fees and markup"""
        provider = self.providers[provider_name]
        services = provider.get_services()
        
        # Find service details
        service = next((s for s in services if s["service"] == service_id), None)
        if not service:
            raise ValueError(f"Service {service_id} not found")
        
        # Calculate base cost
        base_cost = float(service["rate"]) * quantity
        
        # Calculate PayPal fee
        if base_cost < 10:  # Micropayment
            paypal_fee = (base_cost * 0.049) + 0.09
        else:  # Standard rate
            paypal_fee = (base_cost * 0.034) + 0.30
        
        # Platform markup (20%)
        markup = base_cost * 0.20
        
        # Total cost
        total_cost = base_cost + paypal_fee + markup
        
        return {
            "service_name": service["name"],
            "base_cost": base_cost,
            "paypal_fee": paypal_fee,
            "markup": markup,
            "total_cost": round(total_cost, 2),
            "currency": "USD",
            "provider": provider_name,
            "service_details": service
        }
    
    def create_order(self, user_id: str, provider_name: str, service_id: int,
                    target_link: str, quantity: int) -> Dict:
        """Create new SMM order with PayPal payment"""
        # Calculate pricing
        pricing = self.calculate_pricing(provider_name, service_id, quantity)
        
        # Generate order ID
        order_id = hashlib.md5(
            f"{user_id}_{provider_name}_{service_id}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # Create PayPal payment
        paypal_payment = self.paypal.create_payment(
            amount=pricing["total_cost"],
            description=f"SMM Service: {pricing['service_name']} x{quantity}",
            return_url=f"https://yoursite.com/payment/success?order={order_id}",
            cancel_url=f"https://yoursite.com/payment/cancel?order={order_id}"
        )
        
        # Store order details
        order_data = {
            "order_id": order_id,
            "user_id": user_id,
            "provider": provider_name,
            "service_id": service_id,
            "target_link": target_link,
            "quantity": quantity,
            "pricing": pricing,
            "paypal_order_id": paypal_payment["id"],
            "status": OrderStatus.CREATED.value,
            "payment_status": PaymentStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "provider_order_id": None
        }
        
        self.orders[order_id] = order_data
        
        # Get PayPal approval URL
        approval_url = next(
            link["href"] for link in paypal_payment["links"] 
            if link["rel"] == "approve"
        )
        
        return {
            "order_id": order_id,
            "total_cost": pricing["total_cost"],
            "paypal_approval_url": approval_url,
            "order_details": order_data
        }
    
    def process_payment_success(self, order_id: str, paypal_order_id: str) -> Dict:
        """Process successful PayPal payment and execute SMM order"""
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        try:
            # Capture PayPal payment
            capture_result = self.paypal.capture_payment(paypal_order_id)
            
            if capture_result["status"] == "COMPLETED":
                # Update payment status
                order["payment_status"] = PaymentStatus.COMPLETED.value
                order["paypal_capture_id"] = capture_result["id"]
                order["payment_completed_at"] = datetime.now().isoformat()
                
                # Execute SMM order
                provider = self.providers[order["provider"]]
                smm_result = provider.place_order(
                    service_id=order["service_id"],
                    link=order["target_link"],
                    quantity=order["quantity"]
                )
                
                # Update order with provider details
                order["provider_order_id"] = smm_result["order"]
                order["status"] = OrderStatus.PROCESSING.value
                order["smm_order_placed_at"] = datetime.now().isoformat()
                
                logger.info(f"Order {order_id} successfully processed")
                
                return {
                    "success": True,
                    "order_id": order_id,
                    "provider_order_id": smm_result["order"],
                    "status": "processing",
                    "message": "Payment successful, SMM order is being processed"
                }
            else:
                order["payment_status"] = PaymentStatus.FAILED.value
                raise Exception(f"PayPal payment capture failed: {capture_result}")
                
        except Exception as e:
            order["payment_status"] = PaymentStatus.FAILED.value
            order["error_message"] = str(e)
            logger.error(f"Payment processing failed for order {order_id}: {str(e)}")
            
            return {
                "success": False,
                "order_id": order_id,
                "error": str(e)
            }
    
    def check_order_status(self, order_id: str) -> Dict:
        """Check current order status"""
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        if order["provider_order_id"] and order["status"] == OrderStatus.PROCESSING.value:
            try:
                # Check status with provider
                provider = self.providers[order["provider"]]
                provider_status = provider.get_order_status(order["provider_order_id"])
                
                # Update order status based on provider response
                if provider_status["status"] == "Completed":
                    order["status"] = OrderStatus.COMPLETED.value
                elif provider_status["status"] == "Partial":
                    order["status"] = OrderStatus.PARTIAL.value
                elif provider_status["status"] == "Canceled":
                    order["status"] = OrderStatus.CANCELED.value
                
                order["last_status_check"] = datetime.now().isoformat()
                order["provider_status_details"] = provider_status
                
            except Exception as e:
                logger.error(f"Failed to check provider status for order {order_id}: {str(e)}")
        
        return order
    
    def get_user_orders(self, user_id: str) -> List[Dict]:
        """Get all orders for a user"""
        user_orders = [
            order for order in self.orders.values() 
            if order["user_id"] == user_id
        ]
        return sorted(user_orders, key=lambda x: x["created_at"], reverse=True)
    
    def process_refund(self, order_id: str, reason: str = "") -> Dict:
        """Process refund for an order"""
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        if order["payment_status"] != PaymentStatus.COMPLETED.value:
            raise ValueError("Cannot refund order that hasn't been paid")
        
        try:
            # In a real implementation, you would call PayPal refund API
            # For now, we'll simulate the refund
            
            order["payment_status"] = PaymentStatus.REFUNDED.value
            order["refund_reason"] = reason
            order["refunded_at"] = datetime.now().isoformat()
            
            # Cancel order with provider if possible
            provider_config = self.providers[order["provider"]].config
            if provider_config.get("supports_cancel") and order["provider_order_id"]:
                try:
                    provider = self.providers[order["provider"]]
                    # Implement cancel logic here
                    logger.info(f"Canceled provider order {order['provider_order_id']}")
                except Exception as e:
                    logger.warning(f"Failed to cancel provider order: {str(e)}")
            
            return {
                "success": True,
                "order_id": order_id,
                "refund_amount": order["pricing"]["total_cost"],
                "message": "Refund processed successfully"
            }
            
        except Exception as e:
            logger.error(f"Refund processing failed for order {order_id}: {str(e)}")
            return {
                "success": False,
                "order_id": order_id,
                "error": str(e)
            }

# Example usage and testing
def main():
    """Example usage of the SMM Panel Manager"""
    
    # Initialize with PayPal credentials (sandbox)
    panel_manager = SMMPanelManager(
        paypal_client_id="YOUR_PAYPAL_CLIENT_ID",
        paypal_client_secret="YOUR_PAYPAL_CLIENT_SECRET",
        sandbox=True
    )
    
    try:
        # Example: Create an order for Instagram followers
        print("Creating SMM order...")
        order_result = panel_manager.create_order(
            user_id="user123",
            provider_name="goupsocial",
            service_id=1,  # Instagram followers service
            target_link="https://instagram.com/username",
            quantity=1000
        )
        
        print(f"Order created: {order_result['order_id']}")
        print(f"Total cost: ${order_result['total_cost']}")
        print(f"PayPal approval URL: {order_result['paypal_approval_url']}")
        
        # Simulate successful payment (in real scenario, this happens after user approval)
        order_id = order_result['order_id']
        paypal_order_id = panel_manager.orders[order_id]['paypal_order_id']
        
        # Process payment success
        print("\nProcessing payment...")
        payment_result = panel_manager.process_payment_success(order_id, paypal_order_id)
        print(f"Payment result: {payment_result}")
        
        # Check order status
        print("\nChecking order status...")
        status = panel_manager.check_order_status(order_id)
        print(f"Current status: {status['status']}")
        
        # Get user orders
        print("\nUser orders:")
        user_orders = panel_manager.get_user_orders("user123")
        for order in user_orders:
            print(f"- Order {order['order_id']}: {order['status']} (${order['pricing']['total_cost']})")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
