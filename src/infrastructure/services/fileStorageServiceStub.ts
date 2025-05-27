import { IFileStorageService } from '../../domain/services/fileStorageService';
import logger from '../../config/logger';

// Stub implementation of the file storage service
export class FileStorageServiceStub implements IFileStorageService {
  private storage: Map<string, { data: Buffer; metadata: Record<string, any> }> = new Map();

  async uploadFile(fileData: Buffer, fileName: string, metadata?: Record<string, any>): Promise<string> {
    logger.info('uploadFile called with fileName:', fileName);
    const fileId = this.generateFileId();
    this.storage.set(fileId, { data: fileData, metadata: metadata || {} });
    return fileId;
  }

  async downloadFile(fileId: string): Promise<Buffer> {
    logger.info('downloadFile called with fileId:', fileId);
    const file = this.storage.get(fileId);
    if (!file) {
      throw new Error('File not found');
    }
    return file.data;
  }

  async deleteFile(fileId: string): Promise<void> {
    logger.info('deleteFile called with fileId:', fileId);
    this.storage.delete(fileId);
  }

  async getFileMetadata(fileId: string): Promise<Record<string, any>> {
    logger.info('getFileMetadata called with fileId:', fileId);
    const file = this.storage.get(fileId);
    if (!file) {
      throw new Error('File not found');
    }
    return file.metadata;
  }

  private generateFileId(): string {
    return Math.random().toString(36).substr(2, 9);
  }
}