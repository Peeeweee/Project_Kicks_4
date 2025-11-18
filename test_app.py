from dashboard import create_app

app = create_app()
print('Flask app created successfully')
print('\nRegistered blueprints:')
for bp in app.blueprints:
    print(f'  - {bp}')

print('\nURL Map:')
for rule in app.url_map.iter_rules():
    if 'ml_prediction' in rule.endpoint or 'ml-prediction' in str(rule):
        print(f'  {rule.endpoint}: {rule}')
