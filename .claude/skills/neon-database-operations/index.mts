import { Skill } from '@speculative/skill'
import { create_async_engine, AsyncEngine } from 'sqlalchemy/ext/asyncio'
import { select } from 'sqlalchemy/select'
import { SQLModel } from 'sqlmodel'
import { Depends } from 'fastapi'
import { AsyncSession } from 'sqlalchemy/ext/asyncio'

/**
 * Neon Database Operations Skill
 * Handles Neon Serverless PostgreSQL connections and SQLModel queries with data isolation
 */
export const neonDatabaseOperations: Skill = {
  name: 'neon-database-operations',
  description: 'Neon Serverless PostgreSQL connections and SQLModel queries with user isolation',
  version: '1.0.0',

  /**
   * Creates an async engine for Neon PostgreSQL connection
   * @param connectionString - Neon connection string
   * @param poolSize - Connection pool size (default: 10)
   * @param maxOverflow - Maximum overflow connections (default: 20)
   * @returns AsyncEngine instance
   */
  createAsyncEngine: (
    connectionString: string,
    poolSize: number = 10,
    maxOverflow: number = 20
  ): AsyncEngine => {
    return create_async_engine(connectionString, {
      pool_size: poolSize,
      max_overflow: maxOverflow,
      pool_pre_ping: true,  // Verify connections before use
      pool_recycle: 300,    // Recycle connections every 5 minutes
      echo: false           // Set to true for debugging
    })
  },

  /**
   * Creates a dependency function for FastAPI to get database session
   * @param engine - Async engine instance
   * @returns Dependency function for FastAPI
   */
  createSessionDependency: (engine: AsyncEngine) => {
    const get_db_session = async (): Promise<AsyncSession> => {
      const session = new AsyncSession(engine);
      try {
        return session;
      } catch (error) {
        console.error('Failed to create database session:', error);
        throw error;
      }
    };

    return Depends(get_db_session);
  },

  /**
   * Executes a user-filtered SQLModel query with proper error handling
   * @param session - Database session
   * @param model - SQLModel class to query
   * @param authenticatedUserId - ID of authenticated user
   * @param additionalFilters - Additional WHERE conditions (optional)
   * @returns Query results
   */
  executeUserFilteredQuery: async (
    session: AsyncSession,
    model: typeof SQLModel,
    authenticatedUserId: string | number,
    additionalFilters?: any
  ) => {
    try {
      let query = select(model).where(model.user_id === authenticatedUserId);

      // Add additional filters if provided
      if (additionalFilters) {
        query = query.where(additionalFilters);
      }

      const result = await session.execute(query);
      return result.scalars().all();
    } catch (error) {
      console.error('Database query error:', error);
      throw new Error('Failed to execute database query');
    }
  },

  /**
   * Executes a single user-filtered SQLModel query
   * @param session - Database session
   * @param model - SQLModel class to query
   * @param authenticatedUserId - ID of authenticated user
   * @param id - ID of the specific record
   * @returns Single record or null
   */
  executeSingleUserFilteredQuery: async (
    session: AsyncSession,
    model: typeof SQLModel,
    authenticatedUserId: string | number,
    id: string | number
  ) => {
    try {
      const query = select(model)
        .where(model.user_id === authenticatedUserId)
        .where(model.id === id);

      const result = await session.execute(query);
      return result.scalar_one_or_none();
    } catch (error) {
      console.error('Database query error:', error);
      throw new Error('Failed to execute database query');
    }
  },

  /**
   * Creates a new record with user association
   * @param session - Database session
   * @param modelInstance - Instance of SQLModel to create
   * @param authenticatedUserId - ID of authenticated user
   * @returns Created record
   */
  createRecordWithUserAssociation: async (
    session: AsyncSession,
    modelInstance: SQLModel,
    authenticatedUserId: string | number
  ) => {
    try {
      // Ensure the record is associated with the authenticated user
      (modelInstance as any).user_id = authenticatedUserId;

      session.add(modelInstance);
      await session.commit();
      await session.refresh(modelInstance);

      return modelInstance;
    } catch (error) {
      console.error('Database create error:', error);
      await session.rollback();
      throw new Error('Failed to create record');
    }
  },

  /**
   * Updates a user-owned record
   * @param session - Database session
   * @param modelClass - SQLModel class
   * @param recordId - ID of the record to update
   * @param authenticatedUserId - ID of authenticated user
   * @param updateData - Data to update
   * @returns Updated record or null if not found
   */
  updateUserOwnedRecord: async (
    session: AsyncSession,
    modelClass: typeof SQLModel,
    recordId: string | number,
    authenticatedUserId: string | number,
    updateData: any
  ) => {
    try {
      // First verify the record exists and belongs to the user
      const existingRecordResult = await session.execute(
        select(modelClass)
          .where(modelClass.id === recordId)
          .where(modelClass.user_id === authenticatedUserId)
      );

      const record = existingRecordResult.scalar_one_or_none();

      if (!record) {
        return null;  // Record not found or doesn't belong to user
      }

      // Update the record with provided data
      for (const [key, value] of Object.entries(updateData)) {
        if (Object.prototype.hasOwnProperty.call(record, key) && key !== 'user_id') {  // Prevent user_id changes
          (record as any)[key] = value;
        }
      }

      await session.commit();
      await session.refresh(record);

      return record;
    } catch (error) {
      console.error('Database update error:', error);
      await session.rollback();
      throw new Error('Failed to update record');
    }
  },

  /**
   * Deletes a user-owned record
   * @param session - Database session
   * @param modelClass - SQLModel class
   * @param recordId - ID of the record to delete
   * @param authenticatedUserId - ID of authenticated user
   * @returns Boolean indicating success
   */
  deleteUserOwnedRecord: async (
    session: AsyncSession,
    modelClass: typeof SQLModel,
    recordId: string | number,
    authenticatedUserId: string | number
  ) => {
    try {
      // First verify the record exists and belongs to the user
      const existingRecordResult = await session.execute(
        select(modelClass)
          .where(modelClass.id === recordId)
          .where(modelClass.user_id === authenticatedUserId)
      );

      const record = existingRecordResult.scalar_one_or_none();

      if (!record) {
        return false;  // Record not found or doesn't belong to user
      }

      await session.delete(record);
      await session.commit();

      return true;
    } catch (error) {
      console.error('Database delete error:', error);
      await session.rollback();
      throw new Error('Failed to delete record');
    }
  },

  /**
   * Executes a transaction with proper error handling
   * @param session - Database session
   * @param transactionFn - Function to execute in transaction
   * @returns Transaction result
   */
  executeTransaction: async (
    session: AsyncSession,
    transactionFn: (txSession: AsyncSession) => Promise<any>
  ) => {
    try {
      await session.begin();  // Begin transaction

      const result = await transactionFn(session);

      await session.commit();  // Commit transaction
      return result;
    } catch (error) {
      console.error('Database transaction error:', error);
      await session.rollback();  // Rollback on error
      throw new Error('Database transaction failed');
    }
  },

  /**
   * Checks if a record belongs to a user
   * @param session - Database session
   * @param modelClass - SQLModel class
   * @param recordId - ID of the record to check
   * @param authenticatedUserId - ID of authenticated user
   * @returns Boolean indicating ownership
   */
  checkRecordOwnership: async (
    session: AsyncSession,
    modelClass: typeof SQLModel,
    recordId: string | number,
    authenticatedUserId: string | number
  ): Promise<boolean> => {
    try {
      const result = await session.execute(
        select(modelClass)
          .where(modelClass.id === recordId)
          .where(modelClass.user_id === authenticatedUserId)
      );

      return result.scalar_one_or_none() !== null;
    } catch (error) {
      console.error('Ownership check error:', error);
      return false;
    }
  },

  /**
   * Generic query builder with user filtering
   * @param session - Database session
   * @param model - SQLModel class to query
   * @param authenticatedUserId - ID of authenticated user
   * @param options - Query options (filters, pagination, etc.)
   * @returns Query results
   */
  buildUserFilteredQuery: async (
    session: AsyncSession,
    model: typeof SQLModel,
    authenticatedUserId: string | number,
    options: {
      filters?: any,
      orderBy?: any,  // Could be a Column or string
      limit?: number,
      offset?: number
    } = {}
  ) => {
    try {
      let query = select(model).where(model.user_id === authenticatedUserId);

      // Apply additional filters
      if (options.filters) {
        query = query.where(options.filters);
      }

      // Apply ordering
      if (options.orderBy) {
        // This is a simplified version - in practice you'd want to validate the column name
        query = query.order_by(options.orderBy);
      }

      // Apply pagination
      if (options.limit) {
        query = query.limit(options.limit);
      }
      if (options.offset) {
        query = query.offset(options.offset);
      }

      const result = await session.execute(query);
      return result.scalars().all();
    } catch (error) {
      console.error('Database query error:', error);
      throw new Error('Failed to execute database query');
    }
  }
}

export default neonDatabaseOperations