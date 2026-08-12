#!/usr/bin/env python3
"""
Daily Air-Cooled Porsche Image Rotation System for Porsche Digest

Returns a deterministic image based on date so each day gets a unique Porsche air-cooled photo.
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Curated collection of air-cooled Porsche hero images
AIRCOOLED_HERO_IMAGES = [
    {
        "title": "What is the Porsche 911 (type 993)?",
        "image_url": "https://content-hub.imgix.net/GUhocLc6D6V9qFtm3Oc2g/19e093064c8a22f6214f16a85469aac2/7-20things-20you-20need-20to-20know-20about-20the-20porsche-20911-20type-20993.jpg?w=1920",
        "source": "Porsche Stories",
        "description": "The last air-cooled 911 generation in its natural habitat.",
        "model": "911 (993)"
    },
    {
        "title": "What's the best engine oil for my classic Porsche?",
        "image_url": "https://content-hub.imgix.net/7Jbfc1Bipxe77PnjOVNaTU/894ac12e105ead6a7df681de4aec5f8d/what-20is-20the-20best-20engine-20oil.jpg?w=1920",
        "source": "Porsche Stories",
        "description": "Detail shots of classic Porsche air-cooled engines.",
        "model": "911 (964/993)"
    },
    {
        "title": "How to guide to buying a classic Porsche 911",
        "image_url": "https://content-hub.imgix.net/7mr3pIvnvzsRevhgOnB9as/2648ab4764cddc6dfba2a2ee7ba0b485/how-20to-20buy-20a-20classic-20porsche-20911.jpg?w=1920",
        "source": "Porsche Stories",
        "description": "A pristine 911 in a scenic alpine setting.",
        "model": "911 (964)"
    }
]

def get_daily_hero_image(date_str=None):
    """Get today's air-cooled Porsche hero image deterministically."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    random.seed(hash(date_str))
    image = random.choice(AIRCOOLED_HERO_IMAGES)
    
    return {
        'date': date_str,
        **image
    }

if __name__ == "__main__":
    result = get_daily_hero_image()
    print(json.dumps(result, indent=2))
    
    # Save to file for HTML generator
    with open(Path.cwd() / "daily_hero.json", 'w') as f:
        json.dump(result, f, indent=2)
    print("\nSaved to daily_hero.json")