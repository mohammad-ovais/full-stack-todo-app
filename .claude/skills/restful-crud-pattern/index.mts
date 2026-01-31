import { Skill } from '@speculative/skill'

/**
 * RESTful CRUD API Pattern Skill
 * Implements consistent RESTful API patterns for todo tasks with JWT authentication
 */
export const restfulCrudPattern: Skill = {
  name: 'restful-crud-pattern',
  description: 'Consistent RESTful API patterns for todo tasks with JWT authentication',
  version: '1.0.0',

  /**
   * Creates a complete RESTful API controller with all 6 endpoints
   * @param config Configuration for the API endpoints
   * @returns Object containing all 6 RESTful endpoints
   */
  createController: (config: {
    modelName: string,
    tableName: string,
    jwtService: any,
    dbService: any,
    validationSchema?: any
  }) => {
    const { modelName, tableName, jwtService, dbService, validationSchema } = config

    return {
      /**
       * GET /api/{user_id}/tasks - List all tasks for authenticated user
       */
      list: async (req: any, res: any) => {
        try {
          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Query database for user's tasks
          const tasks = await dbService.findAll({
            table: tableName,
            where: { user_id: userId },
            orderBy: { created_at: 'desc' }
          })

          res.status(200).json({
            success: true,
            count: tasks.length,
            data: tasks
          })
        } catch (error) {
          console.error(`Error listing ${modelName}:`, error)
          res.status(500).json({
            error: `Failed to retrieve ${modelName}`,
            details: error.message
          })
        }
      },

      /**
       * POST /api/{user_id}/tasks - Create a new task for authenticated user
       */
      create: async (req: any, res: any) => {
        try {
          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Validate request body if schema is provided
          if (validationSchema) {
            const { error, value } = validationSchema.validate(req.body)
            if (error) {
              return res.status(400).json({
                error: 'Validation failed',
                details: error.details
              })
            }
            req.body = value
          }

          // Prepare task data with user association
          const taskData = {
            ...req.body,
            user_id: userId,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }

          // Insert into database
          const newTask = await dbService.create({
            table: tableName,
            data: taskData
          })

          res.status(201).json({
            success: true,
            message: `${modelName} created successfully`,
            data: newTask
          })
        } catch (error) {
          console.error(`Error creating ${modelName}:`, error)
          res.status(500).json({
            error: `Failed to create ${modelName}`,
            details: error.message
          })
        }
      },

      /**
       * GET /api/{user_id}/tasks/{id} - Get a specific task for authenticated user
       */
      getOne: async (req: any, res: any) => {
        try {
          const { id } = req.params

          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Find the specific task that belongs to the user
          const task = await dbService.findOne({
            table: tableName,
            where: { id: parseInt(id), user_id: userId }
          })

          if (!task) {
            return res.status(404).json({
              error: `${modelName} not found or does not belong to user`
            })
          }

          res.status(200).json({
            success: true,
            data: task
          })
        } catch (error) {
          console.error(`Error getting ${modelName}:`, error)
          res.status(500).json({
            error: `Failed to retrieve ${modelName}`,
            details: error.message
          })
        }
      },

      /**
       * PUT /api/{user_id}/tasks/{id} - Update a specific task for authenticated user
       */
      update: async (req: any, res: any) => {
        try {
          const { id } = req.params

          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Validate request body if schema is provided
          if (validationSchema) {
            const { error, value } = validationSchema.validate(req.body)
            if (error) {
              return res.status(400).json({
                error: 'Validation failed',
                details: error.details
              })
            }
            req.body = value
          }

          // Verify the task exists and belongs to the user
          const existingTask = await dbService.findOne({
            table: tableName,
            where: { id: parseInt(id), user_id: userId }
          })

          if (!existingTask) {
            return res.status(404).json({
              error: `${modelName} not found or does not belong to user`
            })
          }

          // Prepare update data
          const updateData = {
            ...req.body,
            updated_at: new Date().toISOString()
          }

          // Update the task
          const updatedTask = await dbService.update({
            table: tableName,
            where: { id: parseInt(id) },
            data: updateData
          })

          res.status(200).json({
            success: true,
            message: `${modelName} updated successfully`,
            data: updatedTask
          })
        } catch (error) {
          console.error(`Error updating ${modelName}:`, error)
          res.status(500).json({
            error: `Failed to update ${modelName}`,
            details: error.message
          })
        }
      },

      /**
       * DELETE /api/{user_id}/tasks/{id} - Delete a specific task for authenticated user
       */
      delete: async (req: any, res: any) => {
        try {
          const { id } = req.params

          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Verify the task exists and belongs to the user
          const existingTask = await dbService.findOne({
            table: tableName,
            where: { id: parseInt(id), user_id: userId }
          })

          if (!existingTask) {
            return res.status(404).json({
              error: `${modelName} not found or does not belong to user`
            })
          }

          // Delete the task
          await dbService.delete({
            table: tableName,
            where: { id: parseInt(id) }
          })

          res.status(200).json({
            success: true,
            message: `${modelName} deleted successfully`
          })
        } catch (error) {
          console.error(`Error deleting ${modelName}:`, error)
          res.status(500).json({
            error: `Failed to delete ${modelName}`,
            details: error.message
          })
        }
      },

      /**
       * PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion status of a task
       */
      toggleComplete: async (req: any, res: any) => {
        try {
          const { id } = req.params

          // Extract and validate user_id from JWT
          const token = req.headers.authorization?.split(' ')[1]
          if (!token) {
            return res.status(401).json({ error: 'Authorization token required' })
          }

          const decoded = await jwtService.verify(token)
          const userId = decoded.user_id

          // Validate that the URL user_id matches the token user_id
          if (req.params.user_id !== userId.toString()) {
            return res.status(403).json({ error: 'Forbidden: User ID mismatch' })
          }

          // Verify the task exists and belongs to the user
          const existingTask = await dbService.findOne({
            table: tableName,
            where: { id: parseInt(id), user_id: userId }
          })

          if (!existingTask) {
            return res.status(404).json({
              error: `${modelName} not found or does not belong to user`
            })
          }

          // Toggle the completed status
          const newCompletedStatus = !existingTask.completed

          // Update the completion status
          const updatedTask = await dbService.update({
            table: tableName,
            where: { id: parseInt(id) },
            data: {
              completed: newCompletedStatus,
              updated_at: new Date().toISOString()
            }
          })

          res.status(200).json({
            success: true,
            message: `${modelName} completion status updated`,
            data: {
              ...updatedTask,
              completed: newCompletedStatus
            }
          })
        } catch (error) {
          console.error(`Error toggling ${modelName} completion:`, error)
          res.status(500).json({
            error: `Failed to update ${modelName} completion status`,
            details: error.message
          })
        }
      }
    }
  },

  /**
   * Standard middleware for JWT authentication
   */
  authenticateJWT: (jwtService: any) => {
    return async (req: any, res: any, next: any) => {
      try {
        const token = req.headers.authorization?.split(' ')[1]

        if (!token) {
          return res.status(401).json({ error: 'Access token required' })
        }

        const decoded = await jwtService.verify(token)
        req.user = decoded
        next()
      } catch (error) {
        return res.status(403).json({ error: 'Invalid or expired token' })
      }
    }
  },

  /**
   * Helper to validate user ownership of a resource
   */
  validateOwnership: async (dbService: any, tableName: string, resourceId: number, userId: string | number) => {
    const record = await dbService.findOne({
      table: tableName,
      where: { id: parseInt(resourceId.toString()), user_id: parseInt(userId.toString()) }
    })

    return !!record
  }
}

export default restfulCrudPattern