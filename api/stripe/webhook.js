// Stripe Webhook Handler
// Handles Stripe events for payment processing and enrollment

import { createHash, createHmac } from 'crypto';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get the raw body for signature verification
    const body = JSON.stringify(req.body);
    const signature = req.headers['stripe-signature'];
    
    // Webhook secret should be loaded from environment variables
    // const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
    const webhookSecret = 'whsec_your_webhook_secret_here'; // Replace with actual secret
    
    // Verify webhook signature
    if (!verifyWebhookSignature(body, signature, webhookSecret)) {
      console.error('Invalid webhook signature');
      return res.status(400).json({ error: 'Invalid signature' });
    }
    
    const event = req.body;
    
    console.log('Stripe webhook received:', event.type);
    
    // Handle different event types
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutCompleted(event.data.object);
        break;
        
      case 'invoice.paid':
        await handleInvoicePaid(event.data.object);
        break;
        
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event.data.object);
        break;
        
      case 'invoice.payment_succeeded':
        await handleRecurringPayment(event.data.object);
        break;
        
      default:
        console.log('Unhandled event type:', event.type);
    }
    
    res.status(200).json({ received: true });
    
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

function verifyWebhookSignature(body, signature, secret) {
  try {
    const elements = signature.split(',');
    const timestamp = elements[0].split('=')[1];
    const signatures = elements.slice(1).map(el => el.split('=')[1]);
    
    const payloadForSigning = timestamp + '.' + body;
    const expectedSignature = createHmac('sha256', secret).update(payloadForSigning).digest('hex');
    
    return signatures.includes(expectedSignature);
  } catch (error) {
    console.error('Signature verification error:', error);
    return false;
  }
}

async function handleCheckoutCompleted(session) {
  console.log('Checkout completed:', session.id);
  
  try {
    // Extract customer and course information
    const customerEmail = session.customer_email || session.customer_details?.email;
    const customerName = session.customer_details?.name;
    const courseId = session.metadata?.courseId || 'soc-analyst-foundations';
    const paymentPlan = session.metadata?.paymentPlan || 'full';
    
    // Enroll user in course
    await enrollUser({
      email: customerEmail,
      name: customerName,
      courseId: courseId,
      paymentPlan: paymentPlan,
      stripeSessionId: session.id,
      customerId: session.customer
    });
    
    // Send welcome email
    await sendWelcomeEmail({
      email: customerEmail,
      name: customerName,
      courseId: courseId
    });
    
    console.log(`User enrolled successfully: ${customerEmail} in ${courseId}`);
    
  } catch (error) {
    console.error('Error handling checkout completion:', error);
  }
}

async function handleInvoicePaid(invoice) {
  console.log('Invoice paid:', invoice.id);
  
  try {
    const customerEmail = invoice.customer_email;
    const subscriptionId = invoice.subscription;
    
    // Keep access active for subscription payments
    await maintainCourseAccess({
      customerEmail: customerEmail,
      subscriptionId: subscriptionId,
      invoiceId: invoice.id
    });
    
  } catch (error) {
    console.error('Error handling invoice payment:', error);
  }
}

async function handleSubscriptionDeleted(subscription) {
  console.log('Subscription deleted:', subscription.id);
  
  try {
    // End course access when subscription is cancelled
    await endCourseAccess({
      subscriptionId: subscription.id,
      customerId: subscription.customer
    });
    
  } catch (error) {
    console.error('Error handling subscription deletion:', error);
  }
}

async function handleRecurringPayment(invoice) {
  console.log('Recurring payment received:', invoice.id);
  
  try {
    // Check if this is the 6th payment for monthly plan
    const subscription = invoice.subscription;
    const paymentNumber = invoice.attempt_count || 1;
    
    // If this is the 6th payment, schedule subscription cancellation
    if (paymentNumber >= 6) {
      await scheduleSubscriptionEnd(subscription);
    }
    
  } catch (error) {
    console.error('Error handling recurring payment:', error);
  }
}

// Placeholder functions for course management
// In production, these would integrate with your course platform

async function enrollUser({ email, name, courseId, paymentPlan, stripeSessionId, customerId }) {
  // Demo implementation - in production, integrate with your LMS
  console.log('Enrolling user:', { email, name, courseId, paymentPlan });
  
  // Store enrollment record
  const enrollment = {
    id: `enrollment_${Date.now()}`,
    email: email,
    name: name,
    courseId: courseId,
    paymentPlan: paymentPlan,
    stripeSessionId: stripeSessionId,
    customerId: customerId,
    enrolledAt: new Date().toISOString(),
    status: 'active'
  };
  
  // In production: save to database
  if (!global.enrollments) {
    global.enrollments = [];
  }
  global.enrollments.push(enrollment);
  
  return enrollment;
}

async function sendWelcomeEmail({ email, name, courseId }) {
  // Demo implementation - in production, use your email service
  console.log('Sending welcome email to:', email);
  
  const emailContent = {
    to: email,
    subject: 'Welcome to TechStep - Your SOC Analyst Journey Begins!',
    body: `
      Hi ${name},
      
      Welcome to TechStep Foundation! Your enrollment in SOC Analyst Foundations has been confirmed.
      
      Course Access: https://student.techstepfoundation.org
      
      Your journey to becoming a cybersecurity professional starts now!
      
      Best regards,
      The TechStep Team
    `
  };
  
  // In production: integrate with email service (SendGrid, AWS SES, etc.)
  return emailContent;
}

async function maintainCourseAccess({ customerEmail, subscriptionId, invoiceId }) {
  console.log('Maintaining course access for:', customerEmail);
  // Update access status in your system
}

async function endCourseAccess({ subscriptionId, customerId }) {
  console.log('Ending course access for subscription:', subscriptionId);
  // Revoke access in your system
}

async function scheduleSubscriptionEnd(subscriptionId) {
  console.log('Scheduling subscription end after 6 payments:', subscriptionId);
  // In production: use Stripe API to cancel subscription after 6 payments
}