// Stripe Checkout Session Creation API Endpoint
// This simulates a server-side endpoint for Stripe Checkout session creation

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { paymentPlan, courseId } = req.body;
    
    // Validate required fields
    if (!paymentPlan || !courseId) {
      return res.status(400).json({ error: 'Missing required fields: paymentPlan and courseId' });
    }

    // Price IDs as specified by the user
    const priceIds = {
      full: 'price_1S5j8SHdhxmQz9FjYDWLFpyd',           // Full payment $2,849
      down: 'price_1S5j8SHdhxmQz9FjK5KQc0HG',           // Down payment $750
      recurring: 'price_1S5j8SHdhxmQz9FjxZR4DjJS'       // Monthly recurring $375
    };

    // Build line items based on payment plan
    let lineItems = [];
    
    if (paymentPlan === 'full') {
      // Single line item for full payment
      lineItems = [
        {
          price: priceIds.full,
          quantity: 1
        }
      ];
    } else if (paymentPlan === 'monthly') {
      // Two line items: down payment + recurring subscription
      lineItems = [
        {
          price: priceIds.down,      // Down payment $750
          quantity: 1
        },
        {
          price: priceIds.recurring, // Monthly $375 x 6
          quantity: 1
        }
      ];
    } else {
      return res.status(400).json({ error: 'Invalid payment plan. Must be "full" or "monthly"' });
    }

    // This would normally create a Stripe Checkout session
    // For demo purposes, we'll return the configuration that would be sent to Stripe
    const sessionConfig = {
      payment_method_types: ['card', 'apple_pay', 'google_pay'],
      line_items: lineItems,
      mode: paymentPlan === 'full' ? 'payment' : 'subscription',
      success_url: `${req.headers.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.origin}/#courses`,
      metadata: {
        courseId: courseId,
        paymentPlan: paymentPlan
      },
      allow_promotion_codes: true,
      billing_address_collection: 'required',
      shipping_address_collection: null,
      customer_creation: 'always',
      payment_intent_data: {
        setup_future_usage: paymentPlan === 'monthly' ? 'off_session' : null
      }
    };

    // For testing purposes, return a mock checkout URL
    // In production, this would be the actual Stripe Checkout session URL
    const mockCheckoutUrl = `https://checkout.stripe.com/c/pay/${paymentPlan}_${courseId}_${Date.now()}`;

    res.status(200).json({
      checkoutUrl: mockCheckoutUrl,
      sessionId: `cs_test_${Date.now()}`,
      config: sessionConfig // For debugging
    });

  } catch (error) {
    console.error('Checkout session creation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}