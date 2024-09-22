document.addEventListener('DOMContentLoaded', function() {
    const donationAmount = document.getElementById('donation-amount');
    const googlePayButtonContainer = document.getElementById('google-pay-button');

    const baseRequest = {
        apiVersion: 2,
        apiVersionMinor: 0
    };

    const allowedCardNetworks = ["AMEX", "DISCOVER", "JCB", "MASTERCARD", "VISA"];
    const allowedCardAuthMethods = ["PAN_ONLY", "CRYPTOGRAM_3DS"];

    const tokenizationSpecification = {
        type: 'PAYMENT_GATEWAY',
        parameters: {
            'gateway': 'stripe',
            'stripe:version': '2020-08-27',
            'stripe:publishableKey': publishableKey  // From template
        }
    };

    const cardPaymentMethod = {
        type: 'CARD',
        parameters: {
            allowedAuthMethods: allowedCardAuthMethods,
            allowedCardNetworks: allowedCardNetworks
        },
        tokenizationSpecification: tokenizationSpecification
    };

    const paymentDataRequest = Object.assign({}, baseRequest);
    paymentDataRequest.allowedPaymentMethods = [cardPaymentMethod];
    paymentDataRequest.transactionInfo = {
        totalPriceStatus: 'FINAL',
        totalPrice: '0.00', // Will be updated dynamically
        currencyCode: 'NZD'
    };
    paymentDataRequest.merchantInfo = {
        merchantId: merchantId,  // From template
        merchantName: merchantName  // From template
    };

    const paymentsClient = new google.payments.api.PaymentsClient({environment: 'PRODUCTION'});

    paymentsClient.isReadyToPay({allowedPaymentMethods: [cardPaymentMethod]})
        .then(function(response) {
            if (response.result) {
                addGooglePayButton();
            }
        })
        .catch(function(err) {
            console.error('Error determining readiness to pay:', err);
        });

    function addGooglePayButton() {
        const button = paymentsClient.createButton({
            onClick: onGooglePaymentButtonClicked,
            allowedPaymentMethods: [cardPaymentMethod]
        });
        googlePayButtonContainer.appendChild(button);
    }

    function onGooglePaymentButtonClicked() {
        const amount = donationAmount.value;
        if (amount < 1) {
            alert('Please enter a valid donation amount.');
            return;
        }
        paymentDataRequest.transactionInfo.totalPrice = amount;
        paymentsClient.loadPaymentData(paymentDataRequest)
            .then(function(paymentData) {
                processPayment(paymentData);
            })
            .catch(function(err) {
                console.error('Error loading payment data:', err);
            });
    }

    function processPayment(paymentData) {
        // Send payment token to server
        fetch('/donate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: paymentData.paymentMethodData.tokenizationData.token,
                amount: paymentData.transactionInfo.totalPrice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Thank you for your donation!');
                donationAmount.value = ''; // Reset the input field
            } else {
                alert('Donation failed: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error processing payment:', error);
            alert('An error occurred. Please try again.');
        });
    }
});