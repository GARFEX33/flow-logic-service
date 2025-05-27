export interface IFileStorageService {
  uploadFile(fileData: Buffer, fileName: string, metadata?: Record<string, any>): Promise<string>;
  downloadFile(fileId: string): Promise<Buffer>;
  deleteFile(fileId: string): Promise<void>;
  getFileMetadata(fileId: string): Promise<Record<string, any>>;
}