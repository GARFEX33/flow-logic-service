export interface IImageProcessingService {
  processImage(imageData: Buffer, options?: Record<string, any>): Promise<Buffer>;
  getImageMetadata(imageData: Buffer): Promise<Record<string, any>>;
  resizeImage(imageData: Buffer, width: number, height: number): Promise<Buffer>;
  convertImageFormat(imageData: Buffer, format: string): Promise<Buffer>;
}