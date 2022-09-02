"use strict"
console.log("checkout")
// Create an instance of the Stripe object with your publishable API key
const stripe = Stripe(stripePublicKey)

console.log(user)
// Disable the button until we have Stripe set up on the page
document.getElementById("payment-submit").disabled = true;

const elements = stripe.elements();
const style = {
  base: {
    color: "#32325d",
    fontFamily: 'Arial, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#32325d"
    }
  },
  invalid: {
    fontFamily: 'Arial, sans-serif',
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};
const card = elements.create("card", { style: style });
// Stripe injects an iframe into the DOM
card.mount("#card-element");
card.on("change", function (event) {
  // Disable the Pay button if there are no card details in the Element
  document.getElementById("payment-submit").disabled = event.empty;
  document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
});
const form = document.getElementById("payment-form");
form.addEventListener("submit", function(event) {
  event.preventDefault();
  const url = '/create-payment-intent/'
  let data = {
    country: document.getElementById('id_country').value,
    city: document.getElementById('c_city').value,
    address: document.getElementById('c_address').value,
    phone_number: document.getElementById('c_phone').value,
    postal_code: document.getElementById('c_zip').value,
  }
  if (user === 'AnonymousUser') {
    data['email'] = `${document.getElementById('email').value}`
    data['password'] = `${document.getElementById('c_password').value}`
    data['first_name'] = `${document.getElementById('f_name').value}`
    data['last_name'] = `${document.getElementById('l_name').value}`
  } else {
    data['email'] = user
  }
  // Complete payment when the submit button is clicked
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data)
  })
    .then(function(result) {
      return result.json();
    })
    .then(function(data) {
      payWithCard(stripe, card, data.clientSecret);
    });
});

// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
const payWithCard = function(stripe, card, clientSecret) {
  loading(true);
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function(result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message);
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id);
      }
    });
};
/* ------- UI helpers ------- */
// Shows a success message when the payment is complete
const orderComplete = function(paymentIntentId) {
  loading(false);
  document
    .querySelector(".result-message a")
    .setAttribute(
      "href",
      "https://dashboard.stripe.com/test/payments/" + paymentIntentId
    );
  document.querySelector(".result-message").classList.remove("hidden");
  document.getElementById("payment-submit").disabled = true;
};
// Show the customer the error from Stripe if their card fails to charge
const showError = function(errorMsgText) {
  loading(false);
  const errorMsg = document.querySelector("#card-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function() {
    errorMsg.textContent = "";
  }, 4000);
};
// Show a spinner on payment submission
const loading = function(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.getElementById("payment-submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.getElementById("payment-submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};