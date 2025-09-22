def handler(request):
    """Handler simples para Vercel"""
    return {
        'statusCode': 200,
        'body': '{"message": "API funcionando"}'
    }