from app.parsers.text_extractor import TextExtractor
from app.parsers.resume_parser import ResumeParser
from app.models.enums import ProcessingStatus


class ResumeProcessingService:

    @staticmethod
    def process(resume):

        try:

            resume.processing_status = ProcessingStatus.PROCESSING

            text = TextExtractor.extract(resume.filepath)

            parsed = ResumeParser.parse(text)

            resume.raw_text = text
            resume.parsed_data = parsed

            resume.processing_status = ProcessingStatus.COMPLETED

        except Exception as e:

            resume.processing_status = ProcessingStatus.FAILED
            resume.processing_error = str(e)

        return resume