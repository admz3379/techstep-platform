// Agreement Storage API Endpoint
// Stores customer agreement data before Stripe checkout

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { 
      course, 
      paymentPlan, 
      customerName, 
      customerEmail, 
      agreementAccepted, 
      ipAddress 
    } = req.body;
    
    // Validate required fields
    if (!course || !paymentPlan || !customerName || !customerEmail || !agreementAccepted) {
      return res.status(400).json({ 
        error: 'Missing required fields: course, paymentPlan, customerName, customerEmail, agreementAccepted' 
      });
    }
    
    if (!agreementAccepted) {
      return res.status(400).json({ 
        error: 'Agreement must be accepted' 
      });
    }
    
    // Create agreement record
    const agreementRecord = {
      id: `agreement_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      course: course,
      paymentPlan: paymentPlan,
      customerName: customerName,
      customerEmail: customerEmail,
      agreementAccepted: true,
      timestamp: new Date().toISOString(),
      ipAddress: ipAddress || req.headers['x-forwarded-for'] || req.connection.remoteAddress,
      userAgent: req.headers['user-agent'],
      sessionData: {
        courseSlug: 'soc-analyst-foundations',
        priceIds: {
          full: 'price_1S5j8SHdhxmQz9FjYDWLFpyd',
          down: 'price_1S5j8SHdhxmQz9FjK5KQc0HG',
          recurring: 'price_1S5j8SHdhxmQz9FjxZR4DjJS'
        }
      }
    };
    
    // In production, store this in your database
    // For demo purposes, we'll simulate storage
    console.log('Agreement stored:', agreementRecord);
    
    // Store in temporary memory (in production, use database)
    if (!global.agreementStore) {
      global.agreementStore = [];
    }
    global.agreementStore.push(agreementRecord);
    
    res.status(200).json({
      success: true,
      agreementId: agreementRecord.id,
      message: 'Agreement stored successfully'
    });

  } catch (error) {
    console.error('Agreement storage error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}