#!/bin/bash

# 🌐 Domain Monitor Script for arabyouthleaders.org
# This script monitors when the domain becomes functional

DOMAIN="arabyouthleaders.org"
EXPECTED_IP="76.76.21.21"
CHECK_INTERVAL=300  # 5 minutes

echo "🌐 Starting Domain Monitor for $DOMAIN"
echo "Expected IP: $EXPECTED_IP"
echo "Check Interval: $CHECK_INTERVAL seconds"
echo "============================================="

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check DNS resolution
    RESOLVED_IP=$(dig +short $DOMAIN @8.8.8.8)
    
    if [ -n "$RESOLVED_IP" ] && [ "$RESOLVED_IP" = "$EXPECTED_IP" ]; then
        echo "✅ [$TIMESTAMP] SUCCESS: $DOMAIN resolves to $RESOLVED_IP"
        
        # Test HTTPS connection
        if curl -s -I https://$DOMAIN | head -n 1 | grep -q "200"; then
            echo "🎉 [$TIMESTAMP] HTTPS WORKING: Website is fully functional!"
            
            # Test website content
            if curl -s https://$DOMAIN | grep -q "Youth Empowerment"; then
                echo "🚀 [$TIMESTAMP] CONTENT VERIFIED: Website content is correct!"
                echo ""
                echo "🎯 DOMAIN IS FULLY FUNCTIONAL! 🎯"
                echo "✅ https://$DOMAIN"
                echo "✅ https://www.$DOMAIN"
                break
            else
                echo "⚠️  [$TIMESTAMP] Content verification failed"
            fi
        else
            echo "⚠️  [$TIMESTAMP] HTTPS not yet working"
        fi
    else
        echo "⏳ [$TIMESTAMP] DNS not resolved. Current: '$RESOLVED_IP'"
    fi
    
    # Check nameservers
    NS_CHECK=$(dig NS $DOMAIN @8.8.8.8 +short)
    if echo "$NS_CHECK" | grep -q "vercel-dns"; then
        echo "✅ [$TIMESTAMP] Nameservers pointing to Vercel"
    else
        echo "⏳ [$TIMESTAMP] Nameservers not yet configured"
    fi
    
    echo "---"
    sleep $CHECK_INTERVAL
done

echo "🎉 Domain monitoring complete! $DOMAIN is fully functional." 