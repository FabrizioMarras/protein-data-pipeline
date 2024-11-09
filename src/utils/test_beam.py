import apache_beam as beam

def run_pipeline():
    with beam.Pipeline() as pipeline:
        words = pipeline | 'Create' >> beam.Create(['Hello', 'Apache', 'Beam'])
        output = words | 'Print' >> beam.Map(print)

if __name__ == '__main__':
    run_pipeline()
