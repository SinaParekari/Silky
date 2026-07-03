import requests

from django.conf import settings


REQUEST_URL = "https://gateway.zibal.ir/v1/request"
VERIFY_URL = "https://gateway.zibal.ir/v1/verify"
START_PAY_URL = "https://gateway.zibal.ir/start/"


class ZibalGateway:
    @staticmethod
    def request_payment(amount: int, order_id: int):
        payload = {
            "merchant": settings.ZIBAL_MERCHANT,
            "amount": int(amount),
            "callbackUrl": settings.ZIBAL_CALLBACK_URL,
            "orderId": order_id,
        }

        try:
            response = requests.post(
                REQUEST_URL,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("result") != 100:
                raise Exception(
                    data.get("message", "Payment request failed.")
                )

            return {
                "success": True,
                "track_id": data["trackId"],
                "payment_url": f"{START_PAY_URL}{data['trackId']}",
                "data": data,
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection to Zibal timed out.",
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Could not connect to Zibal.",
            }

        except requests.exceptions.HTTPError:
            return {
                "success": False,
                "message": "Invalid response from Zibal.",
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }

    @staticmethod
    def verify_payment(track_id: int):
        payload = {
            "merchant": settings.ZIBAL_MERCHANT,
            "trackId": track_id,
        }

        try:
            response = requests.post(
                VERIFY_URL,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("result") != 100:
                return {
                    "success": False,
                    "message": data.get("message", "Verification failed."),
                    "data": data,
                }

            return {
                "success": True,
                "ref_number": data.get("refNumber"),
                "paid_at": data.get("paidAt"),
                "card_number": data.get("cardNumber"),
                "data": data,
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection to Zibal timed out.",
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Could not connect to Zibal.",
            }

        except requests.exceptions.HTTPError:
            return {
                "success": False,
                "message": "Invalid response from Zibal.",
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }