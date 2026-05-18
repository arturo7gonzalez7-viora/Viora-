#!/bin/bash

# VIORA AUTO-DEPLOYMENT SCRIPT
# This script pushes changes to GitHub and triggers Vercel deployment

echo "🚀 DEPLOYING VIORA WEBSITE..."

# Set Vercel token
export VERCEL_TOKEN="vcp_4xZ5GTvJMgBbiHQs65wqDgW7BSNW6pbMATHB9SSQzq6AGkzcjB0FCTdJ"

# GitHub repository path
REPO_PATH="/tmp/viora-temp"
GITHUB_URL="https://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@github.com/arturo7gonzalez7-viora/Viora-.git"

echo "📥 Cloning repository..."
rm -rf $REPO_PATH
git clone $GITHUB_URL $REPO_PATH
cd $REPO_PATH

echo "📤 Pushing to GitHub..."
git push origin main

echo "🌐 Triggering Vercel deployment..."
vercel --prod --yes --token $VERCEL_TOKEN

echo "✅ DEPLOYMENT COMPLETE!"
echo "🌐 Live at: https://viora-deploy.vercel.app"

# Cleanup
cd /root
rm -rf $REPO_PATH

echo "🔥 VIORA WEBSITE IS LIVE! 🔥"