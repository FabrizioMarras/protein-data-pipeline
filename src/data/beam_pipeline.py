import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_beam_pipeline(input_path, process_fn):
    """
    Runs an Apache Beam pipeline that reads from the specified input path,
    processes the data using the provided processing function, and returns
    the result.

    Args:
        input_path (str): The input path to read data from.
        process_fn (function): A function that defines how to process each element.
    """
    # Initialize Apache Beam pipeline options
    pipeline_options = PipelineOptions()

    # Create the Beam pipeline
    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | 'Read from Input' >> beam.io.ReadFromText(input_path)
            | 'Process Data' >> beam.Map(process_fn)
            # Add more transformations here if needed
        )
