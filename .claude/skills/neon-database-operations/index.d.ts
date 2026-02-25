// Type definitions for neon-database-operations skill
import { AsyncEngine } from 'sqlalchemy/ext/asyncio';
import { AsyncSession } from 'sqlalchemy/ext/asyncio';
import { SQLModel } from 'sqlmodel';

declare module '@speculative/skill-neon-database-operations' {
  export interface SkillConfig {
    connectionString: string;
    poolSize?: number;
    maxOverflow?: number;
  }

  export interface QueryOptions {
    filters?: any;
    orderBy?: any;
    limit?: number;
    offset?: number;
  }

  export interface NeonDatabaseOperations {
    createAsyncEngine: (
      connectionString: string,
      poolSize?: number,
      maxOverflow?: number
    ) => AsyncEngine;

    createSessionDependency: (engine: AsyncEngine) => any; // FastAPI Depends type

    executeUserFilteredQuery: <T extends typeof SQLModel>(
      session: AsyncSession,
      model: T,
      authenticatedUserId: string | number,
      additionalFilters?: any
    ) => Promise<any[]>;

    executeSingleUserFilteredQuery: <T extends typeof SQLModel>(
      session: AsyncSession,
      model: T,
      authenticatedUserId: string | number,
      id: string | number
    ) => Promise<any | null>;

    createRecordWithUserAssociation: (
      session: AsyncSession,
      modelInstance: SQLModel,
      authenticatedUserId: string | number
    ) => Promise<SQLModel>;

    updateUserOwnedRecord: <T extends typeof SQLModel>(
      session: AsyncSession,
      modelClass: T,
      recordId: string | number,
      authenticatedUserId: string | number,
      updateData: any
    ) => Promise<any | null>;

    deleteUserOwnedRecord: <T extends typeof SQLModel>(
      session: AsyncSession,
      modelClass: T,
      recordId: string | number,
      authenticatedUserId: string | number
    ) => Promise<boolean>;

    executeTransaction: (
      session: AsyncSession,
      transactionFn: (txSession: AsyncSession) => Promise<any>
    ) => Promise<any>;

    checkRecordOwnership: <T extends typeof SQLModel>(
      session: AsyncSession,
      modelClass: T,
      recordId: string | number,
      authenticatedUserId: string | number
    ) => Promise<boolean>;

    buildUserFilteredQuery: <T extends typeof SQLModel>(
      session: AsyncSession,
      model: T,
      authenticatedUserId: string | number,
      options?: QueryOptions
    ) => Promise<any[]>;
  }

  const neonDatabaseOperations: NeonDatabaseOperations;

  export default neonDatabaseOperations;
  export { neonDatabaseOperations };
}