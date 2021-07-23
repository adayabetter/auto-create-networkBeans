package com.example.networkdemo.bean

/**
 * @author admin
 * @version 1.0
 * @Description 实体类Result
 * @date 2021-07-23
 */

data class Result (
    
    val date: String,
	val stories: MutableList<Stories>,
	val top_stories: MutableList<Top_stories>
	
    
)
