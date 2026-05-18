import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('image') as File | null

    if (!file) {
      return NextResponse.json({ error: 'No image provided' }, { status: 400 })
    }

    const bytes = await file.arrayBuffer()
    const base64 = Buffer.from(bytes).toString('base64')

    const mimeType = file.type || 'image/jpeg'

    const apiKey = process.env.ANTHROPIC_API_KEY
    if (!apiKey) {
      return NextResponse.json({ error: 'Anthropic API key not configured' }, { status: 500 })
    }

    const today = new Date().toISOString().split('T')[0]

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20241022',
        max_tokens: 1024,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'image',
                source: {
                  type: 'base64',
                  media_type: mimeType,
                  data: base64,
                },
              },
              {
                type: 'text',
                text: `You are a receipt scanner for a restaurant expense tracking system. Extract information from this receipt image and return ONLY a JSON object with these exact fields:
{
  "amount": <number, the total amount paid>,
  "vendor": <string, the business/vendor name>,
  "date": <string, YYYY-MM-DD format, use ${today} if not visible>,
  "category": <string, one of: food_cost, alcohol, labor, rent, utilities, marketing, supplies, other>,
  "description": <string, brief description of what was purchased, max 60 characters>
}

Category guidelines:
- food_cost: groceries, produce, meat, dairy, dry goods for cooking
- alcohol: beer, wine, spirits, mixers
- labor: payroll, staffing services
- rent: rent, lease payments
- utilities: gas, electric, water, internet, phone
- marketing: ads, printing, social media, design
- supplies: cleaning, paper goods, smallwares, packaging
- other: anything that does not fit above

Return ONLY the JSON object, no other text.`,
              },
            ],
          },
        ],
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Anthropic API error:', errorText)
      return NextResponse.json({ error: 'Failed to analyze receipt' }, { status: 500 })
    }

    const result = await response.json()
    const textContent = result.content?.[0]?.text || ''

    // Extract JSON from the response
    const jsonMatch = textContent.match(/\{[\s\S]*\}/)
    if (!jsonMatch) {
      return NextResponse.json({ error: 'Could not parse receipt data' }, { status: 500 })
    }

    const extracted = JSON.parse(jsonMatch[0])

    return NextResponse.json(extracted)
  } catch (err) {
    console.error('Scan receipt error:', err)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
