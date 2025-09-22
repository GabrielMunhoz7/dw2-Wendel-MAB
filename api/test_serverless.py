#!/usr/bin/env python3
import requests, json

BASE = 'https://dw2-wendel-mab.vercel.app/api/coins'

def main():
    print('Testando GET /api/coins ...')
    r = requests.get(BASE, timeout=15)
    print('Status:', r.status_code)
    print('Body:', r.text[:300])

if __name__ == '__main__':
    main()
