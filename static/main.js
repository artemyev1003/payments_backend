// Get Stripe publishable key
let django_config_url = config_url;
fetch(django_config_url)
.then((response) => { return response.json(); })
.then((session) => {
  // Initialize Stripe.js
  const stripe = Stripe(session.publicKey);


// Event handler
document.querySelector("#submitBtn").addEventListener("click", () => {
// Get Checkout Session ID
let django_checkout_url = checkout_url;
fetch(django_checkout_url, {method: 'GET'})
.then((response) => { return response.json(); })
.then((session) => {
  // Redirect to Stripe Checkout
  return stripe.redirectToCheckout({sessionId: session.sessionId})
})
});
});