package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;

import java.io.Serializable;

import cn.edu.tsinghua.thss.popcorn.bean.RepairRecordBean;
import cn.edu.tsinghua.thss.popcorn.ui.LoadingDialog;

/**
 * Created by 兜哥 on 2016/7/20.
 */
public class BadItemActivity extends Activity{
    @ViewInject(R.id.tv_title)
    private TextView tv_title;

    @ViewInject(R.id.tv_time)
    private TextView tv_time;

    @ViewInject(R.id.tv_comment_count)
    private TextView tv_comment_count;

    @ViewInject(R.id.tv_desc)
    private TextView tv_desc;

    @ViewInject(R.id.tv_comment_title)
    private TextView tv_comment_title;

    @ViewInject(R.id.lv_comment)
    private ListView lv_comment;

    @ViewInject(R.id.ll_comment)
    private LinearLayout ll_comment;

    @ViewInject(R.id.et_comment)
    private EditText et_comment;


    private Dialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        progressDialog =  LoadingDialog.createLoadingDialog(this);
        progressDialog.show();
        setContentView(R.layout.bad_item_activity);
        ViewUtils.inject(this);

        initData();

    }

    private void initData() {

        Intent intent=getIntent();
        RepairRecordBean.Info info = (RepairRecordBean.Info) intent.getSerializableExtra("info");
        tv_title.setText(info.title);
        tv_desc.setText(info.description+"\n"+info.device_name+"\n"+info.memo);
        tv_time.setText(info.create_time.substring(0,10));
        tv_comment_count.setText("3");
        tv_comment_title.setText("评论(3)");//应该获取评论的条目数


    }

}
