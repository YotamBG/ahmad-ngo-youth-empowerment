#!/usr/bin/env python3

import json
import sys
from pathlib import Path

def load_lighthouse_results(file_path):
    """Load and parse Lighthouse JSON results"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {file_path}")
        return None

def get_score(data, category):
    """Extract score for a specific category"""
    try:
        return round(data['categories'][category]['score'] * 100)
    except KeyError:
        return "N/A"

def get_metric_value(data, audit_id):
    """Extract specific metric value"""
    try:
        audit = data['audits'][audit_id]
        if audit_id in ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'cumulative-layout-shift']:
            if 'displayValue' in audit:
                return audit['displayValue']
            elif 'numericValue' in audit:
                value = audit['numericValue']
                if audit_id == 'cumulative-layout-shift':
                    return f"{value:.3f}"
                else:
                    return f"{value/1000:.1f}s" if value >= 1000 else f"{value:.0f}ms"
        return audit.get('displayValue', 'N/A')
    except KeyError:
        return "N/A"

def print_comparison_table():
    """Generate comprehensive Lighthouse comparison"""
    
    # Load results
    ahmad_data = load_lighthouse_results('lighthouse-ahmad.json')
    younited_data = load_lighthouse_results('lighthouse-younited.json')
    
    if not ahmad_data or not younited_data:
        return
    
    print("🔥 LIGHTHOUSE PERFORMANCE BENCHMARK COMPARISON")
    print("=" * 80)
    print(f"🌐 Ahmad NGO: {ahmad_data['finalUrl']}")
    print(f"🌐 YOUNITED:  {younited_data['finalUrl']}")
    print("=" * 80)
    
    # Core Lighthouse Scores
    print("\n📊 LIGHTHOUSE SCORES (0-100)")
    print("-" * 50)
    categories = [
        ('performance', 'Performance'),
        ('accessibility', 'Accessibility'), 
        ('best-practices', 'Best Practices'),
        ('seo', 'SEO')
    ]
    
    for cat_id, cat_name in categories:
        ahmad_score = get_score(ahmad_data, cat_id)
        younited_score = get_score(younited_data, cat_id)
        
        # Determine winner
        if ahmad_score == "N/A" or younited_score == "N/A":
            winner = "❓"
        elif ahmad_score > younited_score:
            winner = "🥇"
        elif younited_score > ahmad_score:
            winner = "🥈"
        else:
            winner = "🤝"
            
        print(f"{cat_name:<15} | Ahmad: {ahmad_score:>3} | YOUNITED: {younited_score:>3} | {winner}")
    
    # Performance Metrics Deep Dive
    print("\n⚡ PERFORMANCE METRICS BREAKDOWN")
    print("-" * 50)
    metrics = [
        ('first-contentful-paint', 'First Contentful Paint'),
        ('largest-contentful-paint', 'Largest Contentful Paint'),
        ('speed-index', 'Speed Index'),
        ('total-blocking-time', 'Total Blocking Time'),
        ('cumulative-layout-shift', 'Cumulative Layout Shift')
    ]
    
    for metric_id, metric_name in metrics:
        ahmad_value = get_metric_value(ahmad_data, metric_id)
        younited_value = get_metric_value(younited_data, metric_id)
        print(f"{metric_name:<25} | Ahmad: {ahmad_value:>8} | YOUNITED: {younited_value:>8}")
    
    # Key Optimizations
    print("\n🔧 KEY OPTIMIZATION OPPORTUNITIES")
    print("-" * 50)
    
    # Check specific audits
    optimizations = [
        ('render-blocking-resources', 'Render-blocking resources'),
        ('unused-css-rules', 'Unused CSS'),
        ('unused-javascript', 'Unused JavaScript'),
        ('modern-image-formats', 'Modern image formats'),
        ('efficient-animated-content', 'Animated content optimization')
    ]
    
    for audit_id, audit_name in optimizations:
        try:
            ahmad_audit = ahmad_data['audits'].get(audit_id, {})
            younited_audit = younited_data['audits'].get(audit_id, {})
            
            ahmad_score = ahmad_audit.get('score', 'N/A')
            younited_score = younited_audit.get('score', 'N/A')
            
            if ahmad_score != 'N/A':
                ahmad_score = round(ahmad_score * 100)
            if younited_score != 'N/A':
                younited_score = round(younited_score * 100)
                
            print(f"{audit_name:<30} | Ahmad: {ahmad_score:>3} | YOUNITED: {younited_score:>3}")
        except:
            print(f"{audit_name:<30} | Ahmad: N/A | YOUNITED: N/A")
    
    # Overall Assessment
    print("\n🏆 OVERALL PERFORMANCE ASSESSMENT")
    print("-" * 50)
    
    # Calculate average scores
    ahmad_avg = 0
    younited_avg = 0
    count = 0
    
    for cat_id, _ in categories:
        a_score = get_score(ahmad_data, cat_id)
        y_score = get_score(younited_data, cat_id)
        if a_score != "N/A" and y_score != "N/A":
            ahmad_avg += a_score
            younited_avg += y_score
            count += 1
    
    if count > 0:
        ahmad_avg = round(ahmad_avg / count)
        younited_avg = round(younited_avg / count)
        
        print(f"Ahmad NGO Average Score:     {ahmad_avg}/100")
        print(f"YOUNITED Average Score:      {younited_avg}/100")
        print(f"Performance Gap:             {abs(ahmad_avg - younited_avg)} points")
        
        if ahmad_avg > younited_avg:
            print("🎉 Ahmad NGO WINS! 🥇")
        elif younited_avg > ahmad_avg:
            print("📚 YOUNITED WINS! 🥇")
        else:
            print("🤝 TIE! Both sites perform equally!")
    
    print("\n📈 RECOMMENDATIONS FOR AHMAD NGO:")
    print("-" * 50)
    
    # Performance recommendations based on scores
    perf_score = get_score(ahmad_data, 'performance')
    if perf_score != "N/A" and perf_score < 90:
        print("• 🚀 Optimize loading speed - consider image compression")
        print("• 📦 Minimize JavaScript and CSS bundles")
        print("• 🖼️ Use modern image formats (WebP, AVIF)")
    
    accessibility_score = get_score(ahmad_data, 'accessibility')
    if accessibility_score != "N/A" and accessibility_score < 95:
        print("• ♿ Enhance accessibility - check color contrast")
        print("• 🏷️ Add more descriptive alt texts")
        print("• ⌨️ Improve keyboard navigation")
    
    seo_score = get_score(ahmad_data, 'seo')
    if seo_score != "N/A" and seo_score < 95:
        print("• 🔍 Improve SEO - add meta descriptions")
        print("• 📱 Ensure mobile-friendliness")
        print("• 🔗 Optimize internal linking structure")
    
    print(f"\n💾 Full reports saved to lighthouse-ahmad.json and lighthouse-younited.json")

if __name__ == "__main__":
    print_comparison_table() 