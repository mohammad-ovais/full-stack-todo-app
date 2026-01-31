// Type definitions for restful-crud-pattern skill
declare module '@speculative/skill-restful-crud-pattern' {
  export interface SkillConfig {
    modelName: string;
    tableName: string;
    jwtService: any;
    dbService: any;
    validationSchema?: any;
  }

  export interface TaskController {
    list: (req: any, res: any) => Promise<void>;
    create: (req: any, res: any) => Promise<void>;
    getOne: (req: any, res: any) => Promise<void>;
    update: (req: any, res: any) => Promise<void>;
    delete: (req: any, res: any) => Promise<void>;
    toggleComplete: (req: any, res: any) => Promise<void>;
  }

  export interface RestfulCrudPattern {
    createController: (config: SkillConfig) => TaskController;
    authenticateJWT: (jwtService: any) => (req: any, res: any, next: any) => Promise<void>;
    validateOwnership: (dbService: any, tableName: string, resourceId: number, userId: string | number) => Promise<boolean>;
  }

  const restfulCrudPattern: RestfulCrudPattern;

  export default restfulCrudPattern;
  export { restfulCrudPattern };
}