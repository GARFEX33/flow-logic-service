import { IImageProcessingService } from '../../domain/services/imageProcessingService';
import logger from '../../config/logger';

// Stub implementation of the image processing service
export class ImageProcessingServiceStub implements IImageProcessingService {
  async processImage(imageData: Buffer, options?: Record<string, any>): Promise<Buffer> {
    logger.info('processImage called with options:', options);
    // Return the original image data as a placeholder
    return imageData;
  }

  async getImageMetadata(imageData: Buffer): Promise<Record<string, any>> {
    logger.info('getImageMetadata called');
    // Return dummy metadata as a placeholder
    return {
      width: 800,
      height: 600,
      format: 'JPEG',
    };
  }

  async resizeImage(imageData: Buffer, width: number, height: number): Promise<Buffer> {
    logger.info('resizeImage called with dimensions:', { width, height });
    // Return the original image data as a placeholder
    return imageData;
  }

  async convertImageFormat(imageData: Buffer, format: string): Promise<Buffer> {
    logger.info('convertImageFormat called with format:', format);
    // Return the original image data as a placeholder
    return imageData;
  }
}