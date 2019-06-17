$('#datetimepicker').datepicker({
	language: "zh-CN",
	format:"yyyy-mm-dd"
});

$('.dropmenu').click(function(c){
	c.preventDefault();
	$(this).parent().find("ul").slideToggle();
});


//.btn-yes
$('.sidebar .update-modal-sm .modal-footer .btn-yes').click(function(){
	var num = 1;
	//var oUpdate = $('.sidebar .update-data');
	//var ahref = oUpdate.attr('href');
	
	var timerId = setInterval(function(){
		$('.sidebar .update-modal-sm .modal-body p').text("即将更新数据,请稍后" + num);
		if(num == 0){
			window.location.href = '/updateArticle';
			clearInterval(timerId);
		}
		num--;
	},1000);
});


//模糊查询
(function($){
	$.fn.extend({
		"dropResult":function(options){
			var $Id = $(this);
			$Id.find('#searchWechat').keyup(function(e){
				var last = e.timeStamp;
				setTimeout(function(){
					if(last - e.timeStamp ==0){
						var arr = searchIndex($Id,options);
						loadResult($Id,arr);	
					}
				},500);
			});
		
			$Id.find('#numResult').delegate('.drop-li a','click',function(){
				var html = $(this).html();
				$(this).parents('#numResult').siblings('#searchWechat').val(html);
				$Id.find('#numResult').hide();
			});
		}
	})
	
	function loadResult($Id,arr){
		var html = "";
		var $input = $Id.find('#searchWechat');
		var keywords = $input.val();
		var len = arr.length;
		
		if(len == 0){
			$Id.find('#numResult').hide();
		}else if(len > 20){
			html += '<li class="drop-li"><a href="#">'+keywords+'<small>结果:'+ len +'个</small></a></li>';
		}else{
			$.each(arr, function(idx,value) {
				html+='<li class="drop-li"><a href="#">'+value+'</a></li>';
			});	
		}
		
		$Id.find('#numResult').html(html).show();
	}
	
	function searchIndex($Id,options){
		var $input = $Id.find("#searchWechat");
		var keywords = $input.val();
		var arr = [];
		if(keywords==""||keywords==" "){
			return arr;
		}
		$.each(options, function(idx,obj) {
			if(obj.name.indexOf(keywords)>=0){
				arr.push(obj.name);
			}
		});
		return arr;
	}
})(window.jQuery);


//function loadResult($Id,arr){
		//var html = "";
		//if(arr.length == 0){
		//	$Id.find('#numResult').hide();
		//}
		//$.each(arr, function(idx,value) {
		//	html+='<li class="drop-li"><a href="#">'+value+'</a></li>';
		//});
		//$Id.find('#numResult').html(html).show();
	//}

//搜索功能
$(function(){
	var nowPage = 1,
		pageTol = 0;
	
	function inputData(){
		var DsearchResult = $('#searchWechat').val(),
			Ddate = $('#date').val(),
			DarticleName = $('#articleName').val();
		
		var JinputData = {
			"wechatNum" : DsearchResult,
			"date" : Ddate,
			"articleName" : DarticleName,
			"nowPage" : nowPage
		};
		
		console.log('inputData'+nowPage+"s");
		return JinputData;
	}
	
	
	//ajax renderTable
	function renderTable(){
		var requestData = inputData();
		
		console.log(requestData);
		
		$.ajax({
			url:"result",
			headers: {
	        	'Content-Type': 'application/x-www-form-urlencoded'
	    	},
			type:'POST',
			data:requestData,
			dataType:"json",
			success:function(ajaxReturn){
	    		//var ojson = $.parseJSON(ajaxReturn);
	        	console.log(ajaxReturn);
				var str = "";
				var searchNum = ajaxReturn[0].searchNum;	
				
				$("#resultTable tbody").html("");
				
				for(i in ajaxReturn){
					
				    console.log(ajaxReturn[i].title);
					str += "<tr><td><a id='article-title' href='"+ajaxReturn[i].article_link+"' target='_blank'>" + ajaxReturn[i].title 
									+ "</a></td><td>"
									+ ajaxReturn[i].put_date
									+ "</td><td>"
									+ ajaxReturn[i].from_name
									+ "</td><td>"
									+ ajaxReturn[i].updete_time
									+ "</td></tr>"
				}
				
	            $('.article-board .search-num').text(searchNum);
				$("#resultTable tbody").append(str);
				
				var pageRow = parseInt($(".article-board .h-title .search-num").text()),
					maxRow = ajaxReturn[i].maxRow;
					
				pageTol = getPageTotal(pageRow,maxRow);
				
				nowPage = ajaxReturn[i].nowPage;
				
				renderPage(pageTol,nowPage);
			}
		})
	}
	//搜索
	$('#searchBtn').click(function(){
		renderTable();
	});
	
	//渲染page
	function renderPage(pPageTol,pNowPage){
		var pageTol = pPageTol;//总页数
		var nowPage = pNowPage;//当前页数
		var i = 1;
		var item ="<li id='previousPage'><a href='#' aria-label='Previous'><span aria-hidden='true'>&laquo;上一页</span></a></li>";
		var href = "#";//请求地址
			
		$(".page .pagination").html("");
			
		if(pageTol <= 5){
			for(i;i <= pageTol;i++){
				item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
			}
		}else{	//总页数大于5
			if(nowPage < 5){
				for(i;i <= 5;i++){
					if(i == nowPage){
						item += "<li class='on page-n'><a href='"+href+i+"'>"+i+"</a></li>";
					}else{
						item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
					}
				}
					
				if(nowPage <= pageTol -2){
					item += "<li><span>...</span></li>"
				}
				
			}else{	//当前页大于等于5页
				for(i;i <= 2;i++){
					item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
				}
				item += "<li><span>...</span></li>";
				if(nowPage + 1 ==pageTol){
					for(i = nowPage - 1;i <= pageTol;i++){
						if(i == nowPage){
							item += "<li class='on page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}else{
							item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}
					}
				}else if(nowPage == pageTol){
					for(i = nowPage - 2;i <= pageTol;i++){
						if(i == nowPage){
							item += "<li class='on page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}else{
							item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}
					}
				}else{
					for(i = nowPage -1;i <= nowPage + 1;i++){
						if(i == nowPage){
							item += "<li class='on page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}else{
							item += "<li class='page-n'><a href='"+href+i+"'>"+i+"</a></li>";
						}
					}
					item += "<li><span>...</span></li>"
				}
			
			}
		}
			
		item += "<li id='nextPage'><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;下一页</span></a></li>";
		$('.page .pagination').append(item);
	}
	
	
	//get pageTotal
	function getPageTotal(pageRow,maxRow){
		return Math.ceil(pageRow/maxRow);
	}
	
	//previousPage and nextPage
	
	$(".page .pagination").delegate('#previousPage a','click',function(){
		if(nowPage == 1){
			nowPage = 1;
			return;
		}
		nowPage --;
		renderTable();
	})
		
		
	$(".page .pagination").delegate('#nextPage a','click',function(){
		
		if(nowPage == pageTol){
			nowPage = pageTol;
			return ;
		}
		nowPage++;
		renderTable();
		console.log("nowPage"+nowPage);
		
	})
	
	$(".page .pagination").delegate('.page-n a','click',function(){
		var oText = $(this).text();
		nowPage = parseInt(oText);
		console.log("nowPage"+nowPage);
		renderTable();
	})
	
})






//$(function(){
//	$.ajax({
//		type:"post",
//		url:"http://192.168.1.110:7888/result",
//		async:true,
//	});
//})

//模糊搜索
$(function(){
	$.ajax({
		url:"getMohuInfo",
		type:"post",
		asynv:true,
		//data:{"name":name},
		dataType:"json",
		success:function(data){
			var ajson = data;
			$('.wechat-field').dropResult(ajson);
		}
	})
	
	

})



//接收数据并用table显示
//$(function(){
//	$.ajax({
//		type:"post",
//		datatype:"json",
//		url:,
//		data:,
//		success:function(ajaxReturn){
//			var str = "";
//			$("#resultTable tbody").html("");
//			for(i in ajaxReturn){
//				if(ajaxReturn[i].result == "success"){
//					str += "<tr><td><a id="article-title" href="#">" + ajaxReturn[i].article 
//									+ "</a></td><td>"
//									+ ajaxReturn[i].time
//									+ "</td><td>"
//									+ ajaxReturn[i].wechatNum
//									+ "</td><td>"
//									+ ajaxReturn[i].update
//									+ "</td><tr>"
//				}
//			}
//			$("#resultTable tbody").append(str);
//		}
//	})
//})

//$(function(){
//	var t = $('#resultTable').bootstrapTable({
//		url:'',//
//		method: 'get',
//		datatype:"json",
//		striped:true,
//		undefinedText:"空",
//		pagination:true,
//		showToggle:"true",
//		showColumns:"true",
//		pageNumber:1,
//		pageSize:5,
//		pageList:[5,10,20,40],
//		paginationPreText:'<',
//		paginationNextText:'>',
//		search:false,
//		data_local:"zh-US",
//		sidePagination:"server",
//		queryParams:function(params){
//			return{
//				cp:params.offset,
//				ps:params.limit
//			};
//		},
//		idField:"userID",
//		colums:[
//			{
//				title:'文章标题',
//				field:'articleTitle',
//				align:'center',
//				formatter:function(value,row,index){
//					return'<a id="article-title" href="#"></a>';
//				}
//			},
//			{
//				title:'发布时间',
//				field:'time',
//				align:'center'
//			},
//			{
//				title:'公众号',
//				field:'wechatNum',
//				align:'center'
//			},
//			{
//				title:'点赞数'
//				field：'email',
//				align:'center',
//				formatter:function(value,row,index){
//					return '<span class="glyphicon glyphicon-thumbs-up"></span><span class="like-num">'++'</span>';
//				}
//			},
//		]
//	});
//	
//	t.on('load-success.bs.table',function(data){
//		consolo.log('success');
//		$('')
//	})
//})






//