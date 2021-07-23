package com.example.networkdemo.bean

/**
 * @author admin
 * @version 1.0
 * @Description 实体类Stories
 * @date 2021-07-23
 */

data class Stories (
    
    val image_hue: String,
	val title: String,
	val url: String,
	val hint: String,
	val ga_prefix: String,
	val images: MutableList<String>,
	val type: Int,
	val id: Int
	
    
)
